import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from app.services.api import APIService
from app.services.ai import AIAssistant

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("create_task_without_questions:"))
async def create_task_without_questions(callback: CallbackQuery):
    """Создание задачи без дополнительных вопросов"""
    try:
        # Извлекаем данные задачи из callback_data
        task_data_str = callback.data.split(":", 1)[1]
        import json
        task_data = json.loads(task_data_str)
        
        print(f"CALLBACK: Создаем задачу: {task_data}")
        
        # Создаем задачу через API
        api_service = APIService()
        created_task = await api_service.create_task(task_data, callback.from_user.id)
        
        if created_task:
            success_text = f"✅ <b>Задача создана!</b>\n\n"
            success_text += f"📋 <b>Название:</b> {created_task['title']}\n"
            success_text += f"📝 <b>Описание:</b> {created_task['description']}\n"
            success_text += f"⚡ <b>Приоритет:</b> {created_task['priority']}\n"
            
            if created_task.get('deadline'):
                success_text += f"⏰ <b>Дедлайн:</b> {created_task['deadline']}\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть веб-приложение", web_app={"url": f"{api_service.WEBAPP_URL}"})]
            ])
            
            await callback.message.edit_text(success_text, reply_markup=keyboard)
            await callback.answer("Задача создана!")
        else:
            await callback.message.edit_text("❌ Не удалось создать задачу")
            await callback.answer("Ошибка создания задачи")
            
    except Exception as e:
        logger.error(f"Ошибка создания задачи из callback: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при создании задачи")
        await callback.answer("Ошибка")

@router.callback_query(F.data == "clarify_details")
async def clarify_details(callback: CallbackQuery):
    """Обработка кнопки уточнения деталей"""
    try:
        await callback.message.edit_text(
            "✏️ <b>Уточните детали задачи:</b>\n\n"
            "Отправьте текстовое сообщение с дополнительной информацией:\n"
            "• Дедлайн (когда нужно выполнить)\n"
            "• Приоритет (важно/не важно)\n"
            "• Подробное описание"
        )
        await callback.answer("Ожидаю уточнения...")
        
    except Exception as e:
        logger.error(f"Ошибка обработки уточнения: {e}")
        await callback.answer("Ошибка")

@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Обработка кнопки помощи"""
    help_text = """🆘 <b>Помощь по использованию бота</b>

🎤 <b>Голосовые сообщения:</b>
Отправьте голосовое сообщение с описанием задачи. Например:
"Создай задачу: купить молоко до завтра"

📝 <b>Текстовые сообщения:</b>
Напишите сообщение с ключевыми словами:
• "создай задачу"
• "добавь задачу" 
• "задача"

📸 <b>Фотографии:</b>
Отправьте фото - оно будет прикреплено к задаче

🚀 <b>Веб-приложение:</b>
Нажмите кнопку "Открыть веб-приложение" для управления проектами и задачами"""
    
    await callback.message.edit_text(help_text)
    await callback.answer("Помощь")


@router.callback_query(F.data.startswith("approve:"))
async def approve_request(callback: CallbackQuery):
    """Одобрение запроса через callback кнопку"""
    approval_id = int(callback.data.split(":")[1])
    
    await callback.answer("⏳ Одобряю запрос...")
    
    try:
        api_service = APIService()
        result = await api_service.review_approval(approval_id, "approved")
        
        if result:
            await callback.message.edit_text("✅ Запрос одобрен!")
        else:
            await callback.message.edit_text("❌ Не удалось одобрить запрос")
            
    except Exception as e:
        logger.error(f"Ошибка одобрения запроса: {e}")
        await callback.message.edit_text(f"❌ Ошибка одобрения: {str(e)}")


@router.callback_query(F.data.startswith("reject:"))
async def reject_request(callback: CallbackQuery):
    """Отклонение запроса через callback кнопку"""
    approval_id = int(callback.data.split(":")[1])
    
    await callback.answer("⏳ Отклоняю запрос...")
    
    try:
        api_service = APIService()
        result = await api_service.review_approval(approval_id, "rejected")
        
        if result:
            await callback.message.edit_text("❌ Запрос отклонен!")
        else:
            await callback.message.edit_text("❌ Не удалось отклонить запрос")
            
    except Exception as e:
        logger.error(f"Ошибка отклонения запроса: {e}")
        await callback.message.edit_text(f"❌ Ошибка отклонения: {str(e)}")
