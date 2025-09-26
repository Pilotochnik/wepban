from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from app.services.api import APIService

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user_data: dict = None):
    """Обработчик команды /start"""
    
    # Регистрируем пользователя в системе
    api_service = APIService()
    welcome_text = f"Добро пожаловать, {message.from_user.first_name}.\n\nAI-ассистент для управления проектами. Отправляйте задачи голосом или текстом."
    
    # Создаем клавиатуру - только 2 кнопки
    keyboard_buttons = [
        [InlineKeyboardButton(text="Перейти в проект", web_app={"url": f"{api_service.WEBAPP_URL}"})],
        [InlineKeyboardButton(text="AI чат", callback_data="ai_chat")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(welcome_text, reply_markup=keyboard)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    
    help_text = """🆘 <b>Помощь по использованию бота</b>

🎤 <b>Голосовые сообщения:</b>
Отправьте голосовое сообщение с описанием задачи. Например:
• "Создай задачу: купить корм для офиса до завтра"
• "Важная задача: подготовить презентацию к пятнице"
• "Добавь задачу в проект Маркетинг: создать логотип"

📝 <b>Текстовые сообщения:</b>
Можете просто написать описание задачи текстом.

📸 <b>Фото:</b>
Отправьте фото, и я помогу прикрепить его к задаче.

🌐 <b>Веб-приложение:</b>
Используйте веб-приложение для полноценной работы с Kanban доской.

📋 <b>Доступные команды:</b>
/start - Главное меню
/help - Эта справка
/projects - Мои проекты

🤖 <b>AI ассистент:</b>
Я умею анализировать ваши запросы и создавать структурированные задачи с:
• Названием и описанием
• Приоритетом
• Дедлайном
• Назначением на проект

Если информации недостаточно, я задам уточняющие вопросы!"""
    
    await message.answer(help_text)


@router.callback_query(F.data == "help")
async def callback_help(callback):
    """Обработчик кнопки помощи"""
    await cmd_help(callback.message)
    await callback.answer()


@router.message(Command("projects"))
async def cmd_projects(message: Message):
    """Обработчик команды /projects"""
    api_service = APIService()
    
    try:
        print(f"PROJECTS: Using user ID: {message.from_user.id}")
        projects = await api_service.get_user_projects(message.from_user.id)
        
        if not projects:
            text = "📂 У вас пока нет проектов.\n\nСоздайте первый проект в веб-приложении!"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть веб-приложение", web_app={"url": f"{api_service.WEBAPP_URL}"})]
            ])
        else:
            text = "📂 <b>Ваши проекты:</b>\n\n"
            for project in projects:
                text += f"• <b>{project['name']}</b>\n"
                if project.get('description'):
                    text += f"  {project['description']}\n"
                text += "\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть веб-приложение", web_app={"url": f"{api_service.WEBAPP_URL}"})]
            ])
        
        await message.answer(text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer(f"❌ Ошибка получения проектов: {str(e)}")


@router.callback_query(F.data == "ai_chat")
async def callback_ai_chat(callback):
    """Обработчик кнопки AI чат"""
    ai_chat_text = """AI чат активен.

Отправляйте задачи голосом или текстом. AI автоматически распределит их по проектам.

Примеры:
• "Создай задачу: купить корм для офиса до завтра"
• "Важная задача: подготовить презентацию к пятнице"
• "Добавь задачу в проект Маркетинг: создать логотип"

Просто отправьте сообщение..."""
    
    await callback.message.edit_text(ai_chat_text)
    await callback.answer()

@router.callback_query(F.data == "my_projects")
async def callback_projects(callback):
    """Обработчик кнопки проектов"""
    print(f"CALLBACK: User ID: {callback.from_user.id}")
    print(f"CALLBACK: Bot ID: {callback.bot.id}")
    
    try:
        api_service = APIService()
        projects = await api_service.get_user_projects(callback.from_user.id)
        
        if projects:
            projects_text = "📊 <b>Ваши проекты:</b>\n\n"
            for project in projects:
                projects_text += f"📁 <b>{project['name']}</b>\n"
                if project.get('description'):
                    projects_text += f"   {project['description']}\n"
                projects_text += f"   ID: {project['id']}\n\n"
        else:
            projects_text = "📊 У вас пока нет проектов.\n\nСоздайте проект в веб-приложении!"
        
        await callback.message.edit_text(projects_text)
        
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка получения проектов: {str(e)}")
    
    await callback.answer()
