import logging
import httpx
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from app.services.api import APIService
from typing import Dict, Any

router = Router()
logger = logging.getLogger(__name__)

def is_creator(user_data: Dict[str, Any]) -> bool:
    """Проверка, является ли пользователь создателем"""
    return user_data.get('role') == 'creator'

@router.message(Command("admin"))
async def cmd_admin(message: Message, user_data: Dict[str, Any] = None):
    """Админ-панель для создателя"""
    if not is_creator(user_data):
        await message.answer("❌ Доступ запрещен. Только создатель может использовать админ-панель.")
        return
    
    api_service = APIService()
    
    try:
        # Получаем статистику
        auth_data = await api_service.authenticate_user(message.from_user.id)
        token = auth_data["access_token"]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{api_service.base_url}/api/v1/admin/stats", headers=headers)
            response.raise_for_status()
            stats = response.json()
        
        text = "🔧 <b>Админ-панель</b>\n\n"
        text += f"👥 Всего пользователей: {stats['total_users']}\n"
        text += f"✅ Активных пользователей: {stats['active_users']}\n"
        text += f"👷 Прорабов: {stats['foremen_count']}\n"
        text += f"🔨 Рабочих: {stats['workers_count']}\n"
        text += f"⏳ Ожидающих одобрения: {stats['pending_approvals']}\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👥 Управление пользователями", callback_data="admin_users")],
            [InlineKeyboardButton(text="⏳ Запросы на одобрение", callback_data="admin_approvals")],
            [InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="admin_add_user")],
            [InlineKeyboardButton(text="📊 Обновить статистику", callback_data="admin_refresh")]
        ])
        
        await message.answer(text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        await message.answer(f"❌ Ошибка получения статистики: {str(e)}")

@router.callback_query(F.data == "admin_refresh")
async def admin_refresh(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Обновление статистики"""
    if not is_creator(user_data):
        await callback.answer("❌ Доступ запрещен")
        return
    
    await cmd_admin(callback.message, user_data)
    await callback.answer("Статистика обновлена")

@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Управление пользователями"""
    if not is_creator(user_data):
        await callback.answer("❌ Доступ запрещен")
        return
    
    api_service = APIService()
    
    try:
        # Получаем список пользователей
        auth_data = await api_service.authenticate_user(callback.from_user.id)
        token = auth_data["access_token"]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{api_service.base_url}/api/v1/admin/users", headers=headers)
            response.raise_for_status()
            users = response.json()
        
        text = "👥 <b>Управление пользователями</b>\n\n"
        
        for user in users:
            status = "✅" if user['is_active'] else "❌"
            role_emoji = {
                'creator': '👑',
                'foreman': '👷',
                'worker': '🔨',
                'viewer': '👁️'
            }.get(user['role'], '❓')
            
            text += f"{status} {role_emoji} <b>{user['first_name']} {user['last_name']}</b>\n"
            text += f"   ID: {user['telegram_id']} | Роль: {user['role']}\n"
            text += f"   Username: @{user['username']}\n\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="admin_add_user")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Ошибка получения пользователей: {e}")
        await callback.message.edit_text(f"❌ Ошибка получения пользователей: {str(e)}")

@router.callback_query(F.data == "admin_approvals")
async def admin_approvals(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Запросы на одобрение"""
    if not is_creator(user_data):
        await callback.answer("❌ Доступ запрещен")
        return
    
    api_service = APIService()
    
    try:
        # Получаем запросы на одобрение
        auth_data = await api_service.authenticate_user(callback.from_user.id)
        token = auth_data["access_token"]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{api_service.base_url}/api/v1/admin/approvals/pending", headers=headers)
            response.raise_for_status()
            approvals = response.json()
        
        if not approvals:
            text = "⏳ <b>Запросы на одобрение</b>\n\nНет ожидающих запросов"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        else:
            text = "⏳ <b>Запросы на одобрение</b>\n\n"
            keyboard_buttons = []
            
            for approval in approvals:
                text += f"📋 <b>Запрос #{approval['id']}</b>\n"
                text += f"От: {approval['requester']['first_name']} {approval['requester']['last_name']}\n"
                text += f"Действие: {approval['action_type']}\n"
                text += f"Описание: {approval['description']}\n\n"
                
                keyboard_buttons.append([
                    InlineKeyboardButton(text=f"✅ Одобрить #{approval['id']}", callback_data=f"approve:{approval['id']}"),
                    InlineKeyboardButton(text=f"❌ Отклонить #{approval['id']}", callback_data=f"reject:{approval['id']}")
                ])
            
            keyboard_buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")])
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Ошибка получения запросов: {e}")
        await callback.message.edit_text(f"❌ Ошибка получения запросов: {str(e)}")

@router.callback_query(F.data == "admin_add_user")
async def admin_add_user(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Добавление пользователя"""
    if not is_creator(user_data):
        await callback.answer("❌ Доступ запрещен")
        return
    
    text = "➕ <b>Добавление пользователя</b>\n\n"
    text += "Для добавления пользователя отправьте сообщение в формате:\n"
    text += "<code>/add_user telegram_id:123456789 role:foreman first_name:Иван last_name:Петров username:ivan_petrov</code>\n\n"
    text += "Доступные роли:\n"
    text += "• <code>foreman</code> - Прораб\n"
    text += "• <code>worker</code> - Рабочий\n"
    text += "• <code>viewer</code> - Наблюдатель"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin_back")
async def admin_back(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Возврат в главное меню админки"""
    await cmd_admin(callback.message, user_data)

@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, user_data: Dict[str, Any] = None):
    """Обработчик кнопки админ-панели"""
    await cmd_admin(callback.message, user_data)
    await callback.answer()

@router.message(Command("add_user"))
async def cmd_add_user(message: Message, user_data: Dict[str, Any] = None):
    """Добавление пользователя через команду"""
    if not is_creator(user_data):
        await message.answer("❌ Доступ запрещен. Только создатель может добавлять пользователей.")
        return
    
    # Парсим команду
    args = message.text.split()[1:]  # Убираем /add_user
    user_data_dict = {}
    
    for arg in args:
        if ':' in arg:
            key, value = arg.split(':', 1)
            user_data_dict[key] = value
    
    required_fields = ['telegram_id', 'role', 'first_name', 'last_name']
    missing_fields = [field for field in required_fields if field not in user_data_dict]
    
    if missing_fields:
        await message.answer(f"❌ Недостаточно данных. Отсутствуют: {', '.join(missing_fields)}")
        return
    
    api_service = APIService()
    
    try:
        # Получаем токен создателя
        auth_data = await api_service.authenticate_user(message.from_user.id)
        token = auth_data["access_token"]
        
        # Добавляем пользователя
        user_create_data = {
            'telegram_id': int(user_data_dict['telegram_id']),
            'role': user_data_dict['role'],
            'first_name': user_data_dict['first_name'],
            'last_name': user_data_dict['last_name'],
            'username': user_data_dict.get('username', ''),
            'is_active': True
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(f"{api_service.base_url}/api/v1/admin/users", json=user_create_data, headers=headers)
            response.raise_for_status()
            new_user = response.json()
        
        await message.answer(f"✅ Пользователь успешно добавлен!\n\n"
                           f"👤 {new_user['first_name']} {new_user['last_name']}\n"
                           f"🆔 ID: {new_user['telegram_id']}\n"
                           f"🎭 Роль: {new_user['role']}")
        
    except Exception as e:
        logger.error(f"Ошибка добавления пользователя: {e}")
        await message.answer(f"❌ Ошибка добавления пользователя: {str(e)}")
