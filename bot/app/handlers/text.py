import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.services.ai import AIAssistant
from app.services.api import APIService

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text & ~F.text.startswith('/'))
async def handle_text_message(message: Message):
    """Обработка текстовых сообщений для создания задач (исключая команды)"""
    logger.info(f"TEXT HANDLER: Получено текстовое сообщение от {message.from_user.id}: {message.text}")
    print(f"TEXT HANDLER: Получено текстовое сообщение от {message.from_user.id}: {message.text}")
        
    logger.info(f"TEXT HANDLER: Обрабатываем текстовое сообщение: {message.text}")
    print(f"TEXT HANDLER: Обрабатываем текстовое сообщение: {message.text}")
    
    try:
        # Инициализируем сервисы
        ai_service = AIAssistant()
        api_service = APIService()
        
        # Проверяем, содержит ли сообщение запрос на создание задачи
        task_keywords = ['создай', 'добавь', 'добавить', 'задача', 'задачи', 'todo', 'task']
        message_text = message.text.lower()
        
        print(f"Проверяем ключевые слова в: {message_text}")
        print(f"Ключевые слова: {task_keywords}")
        
        if any(keyword in message_text for keyword in task_keywords):
            print("Найдено ключевое слово, создаем задачу...")
            logger.info(f"Обнаружен запрос на создание задачи: {message.text}")
            
            # Отправляем сообщение о начале обработки
            await message.answer("🤖 Анализирую ваш запрос...")
            
            # Получаем проекты пользователя (может быть пустой список)
            try:
                user_projects = await api_service.get_user_projects(message.from_user.id)
            except Exception as e:
                logger.warning(f"Не удалось получить проекты: {e}")
                user_projects = []  # Используем пустой список
            
            # Используем AI для анализа и создания задачи
            task_data = await ai_service.analyze_text_request(message.text, user_projects)
            
            logger.info(f"AI анализ результата: {task_data}")
            print(f"AI анализ результата: {task_data}")
            
            if task_data.get("status") == "not_task":
                await message.answer("❌ Это не похоже на задачу. Попробуйте написать что-то вроде: \"Создай задачу: купить молоко\"")
            else:
                # AI вернул данные задачи напрямую
                logger.info("Создаем задачу через API...")
                print("Создаем задачу через API...")
                
                # Извлекаем данные задачи из ответа AI
                if "task" in task_data:
                    task_payload = task_data["task"]
                else:
                    task_payload = task_data
                
                print(f"Sending task payload: {task_payload}")
                created_task = await api_service.create_task(task_payload, message.from_user.id)
                
                if created_task:
                    await message.answer(
                        f"✅ Задача создана!\n\n"
                        f"📝 Название: {created_task.get('title', 'Без названия')}\n"
                        f"📋 Описание: {created_task.get('description', 'Без описания')}\n"
                        f"📅 Статус: {created_task.get('status', 'Новая')}\n"
                        f"🏷️ Проект: {created_task.get('project_name', 'Без проекта')}"
                    )
                    logger.info(f"Задача успешно создана: {created_task}")
                else:
                    await message.answer("❌ Не удалось создать задачу. Проверьте, что у вас есть доступные проекты.")
                    logger.error("Не удалось создать задачу через API")
        else:
            # Если это не запрос на создание задачи, отвечаем общим сообщением
            await message.answer(
                "🤖 Я понимаю только запросы на создание задач.\n\n"
                "Попробуйте написать:\n"
                "• \"Создай задачу: купить молоко\"\n"
                "• \"Добавь задачу: позвонить клиенту\"\n"
                "• \"Задача: подготовить презентацию\""
            )
            
    except Exception as e:
        logger.error(f"Ошибка обработки текстового сообщения: {e}", exc_info=True)
        print(f"Ошибка обработки текстового сообщения: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Произошла ошибка при обработке сообщения. Попробуйте еще раз.")
