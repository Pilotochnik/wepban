from aiogram import Router
from aiogram.types import WebAppData, Message

router = Router()


@router.message(lambda message: message.web_app_data is not None)
async def handle_webapp_data(message: Message):
    """Обработка данных из веб-приложения"""
    
    webapp_data: WebAppData = message.web_app_data
    
    # Здесь можно обработать данные, полученные из веб-приложения
    # Например, подтверждение создания задачи или другую информацию
    
    try:
        import json
        data = json.loads(webapp_data.data)
        
        if data.get("action") == "task_created":
            task_title = data.get("task_title", "Задача")
            await message.answer(f"✅ Задача '{task_title}' успешно создана!")
        
        elif data.get("action") == "task_updated":
            task_title = data.get("task_title", "Задача")
            await message.answer(f"📝 Задача '{task_title}' обновлена!")
        
        else:
            await message.answer("📱 Данные получены из веб-приложения")
            
    except Exception as e:
        await message.answer("📱 Веб-приложение отправлено")
