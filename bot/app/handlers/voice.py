from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import tempfile
import os
from app.services.api import APIService
from app.services.ai import AIAssistant

router = Router()


@router.message(F.content_type == "voice")
async def handle_voice_message(message: Message):
    """Обработка голосовых сообщений"""
    
    print(f"VOICE HANDLER: Получено голосовое сообщение от {message.from_user.id}")
    
    # Показываем, что бот обрабатывает сообщение
    processing_msg = await message.answer("🎤 Обрабатываю голосовое сообщение...")
    
    try:
        print("VOICE HANDLER: Начинаем обработку голосового сообщения...")
        
        # Скачиваем голосовое сообщение
        voice = message.voice
        print(f"VOICE HANDLER: Получен файл voice: {voice.file_id}")
        
        file = await message.bot.get_file(voice.file_id)
        print(f"VOICE HANDLER: Файл получен: {file.file_path}")
        
        # Сохраняем во временный файл
        temp_file_path = tempfile.mktemp(suffix=".oga")
        print(f"VOICE HANDLER: Скачиваем файл в: {temp_file_path}")
        
        try:
            # В Aiogram 3.x используем bot.download_file
            await message.bot.download_file(file.file_path, temp_file_path)
            print(f"VOICE HANDLER: Файл успешно скачан: {temp_file_path}")
            
            # Проверяем, что файл существует и не пустой
            if os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
                print(f"VOICE HANDLER: Размер файла: {os.path.getsize(temp_file_path)} байт")
            else:
                print("VOICE HANDLER: ОШИБКА - файл не существует или пустой!")
                await message.answer("❌ Ошибка загрузки голосового сообщения")
                return
                
        except Exception as e:
            print(f"VOICE HANDLER: Ошибка скачивания файла: {e}")
            await message.answer("❌ Ошибка загрузки голосового сообщения")
            return
        
        # Обрабатываем через AI
        ai_assistant = AIAssistant()
        api_service = APIService()
        
        # Получаем проекты пользователя
        print("VOICE HANDLER: Получаем проекты пользователя...")
        projects = await api_service.get_user_projects(message.from_user.id)
        projects_info = [{"id": p["id"], "name": p["name"]} for p in projects]
        print(f"VOICE HANDLER: Проектов найдено: {len(projects)}")
        
        # Анализируем голосовое сообщение
        print("VOICE HANDLER: Запускаем AI анализ...")
        result = await ai_assistant.process_voice_message(temp_file_path, projects_info)
        print(f"VOICE HANDLER: AI результат: {result}")
        
        if result["status"] == "questions_needed":
            # Нужны уточнения
            questions_text = "❓ Мне нужны уточнения:\n\n"
            for i, question in enumerate(result["questions"], 1):
                questions_text += f"{i}. {question}\n"
            
            questions_text += f"\n📝 <b>Предлагаемая задача:</b>\n"
            questions_text += f"• <b>Название:</b> {result['suggested_task']['title']}\n"
            questions_text += f"• <b>Описание:</b> {result['suggested_task']['description']}\n"
            questions_text += f"• <b>Приоритет:</b> {result['suggested_task']['priority']}\n"
            
            questions_text += f"\n🎤 <b>Распознанный текст:</b>\n{result['original_text']}"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Создать задачу", callback_data=f"create_task_without_questions:{result['task_data']}")],
                [InlineKeyboardButton(text="✏️ Уточнить детали", callback_data="clarify_details")]
            ])
            
            await processing_msg.edit_text(questions_text, reply_markup=keyboard)
        
        elif result["status"] == "task_created":
            # Создаем задачу через API
            print("VOICE HANDLER: Создаем задачу через API...")
            task_data = result["task"]
            created_task = await api_service.create_task(task_data, message.from_user.id)
            
            if created_task:
                print(f"VOICE HANDLER: Задача создана: {created_task}")
                # Задача создана
                task = created_task
                success_text = f"✅ <b>Задача создана!</b>\n\n"
                success_text += f"📋 <b>Название:</b> {task['title']}\n"
                success_text += f"📝 <b>Описание:</b> {task['description']}\n"
                success_text += f"⚡ <b>Приоритет:</b> {task['priority']}\n"
                if task.get('deadline'):
                    from datetime import datetime
                    try:
                        # Парсим дату и форматируем
                        deadline = datetime.fromisoformat(task['deadline'].replace('Z', '+00:00'))
                        formatted_deadline = deadline.strftime('%d.%m.%Y %H:%M')
                        success_text += f"⏰ <b>Дедлайн:</b> {formatted_deadline}\n"
                    except:
                        success_text += f"⏰ <b>Дедлайн:</b> {task['deadline']}\n"
                
                # Получаем название проекта
                project_name = "Без проекта"
                if task.get('project_id'):
                    project = next((p for p in projects if p["id"] == task["project_id"]), None)
                    if project:
                        project_name = project["name"]
                success_text += f"📂 <b>Проект:</b> {project_name}\n"
                
                success_text += f"\n🎤 <b>Распознанный текст:</b>\n{result['original_text']}"
                
                print(f"VOICE HANDLER: Отправляем ответ пользователю...")
                print(f"VOICE HANDLER: Текст ответа: {success_text}")
                
                try:
                    # Пытаемся отредактировать сообщение
                    await processing_msg.edit_text(success_text)
                    print("VOICE HANDLER: Ответ успешно отправлен!")
                except Exception as e:
                    print(f"VOICE HANDLER: Ошибка редактирования, отправляем новое сообщение: {e}")
                    try:
                        # Если не удалось отредактировать, отправляем новое сообщение
                        await message.answer(success_text)
                        print("VOICE HANDLER: Новое сообщение отправлено!")
                    except Exception as e2:
                        print(f"VOICE HANDLER: Критическая ошибка отправки: {e2}")
                        # Отправляем краткое сообщение
                        await message.answer("✅ Задача создана! Проверьте веб-приложение.")
            else:
                print("VOICE HANDLER: Задача не была создана")
                await processing_msg.edit_text("❌ Не удалось создать задачу в базе данных")
        
        else:
            await processing_msg.edit_text(f"❌ Ошибка обработки: {result.get('error', 'Неизвестная ошибка')}")
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка обработки голосового сообщения: {str(e)}")
    
    finally:
        # Удаляем временный файл
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.callback_query(F.data.startswith("create_task_without_questions:"))
async def create_task_without_questions(callback: CallbackQuery):
    """Создание задачи без дополнительных уточнений"""
    
    await callback.answer("⏳ Создаю задачу...")
    
    try:
        import json
        task_data = json.loads(callback.data.split(":", 1)[1])
        
        api_service = APIService()
        result = await api_service.create_task_from_ai_data(callback.from_user.id, task_data)
        
        if result["status"] == "success":
            task = result["task"]
            success_text = f"✅ <b>Задача создана!</b>\n\n"
            success_text += f"📋 <b>Название:</b> {task['title']}\n"
            success_text += f"📝 <b>Описание:</b> {task['description']}\n"
            success_text += f"⚡ <b>Приоритет:</b> {task['priority']}\n"
            
            if task.get('deadline'):
                success_text += f"⏰ <b>Дедлайн:</b> {task['deadline']}\n"
            if task.get('project'):
                success_text += f"📂 <b>Проект:</b> {task['project']['name']}\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть веб-приложение", web_app={"url": f"{api_service.WEBAPP_URL}"})]
            ])
            
            await callback.message.edit_text(success_text, reply_markup=keyboard)
        else:
            await callback.message.edit_text(f"❌ Ошибка создания задачи: {result.get('error')}")
    
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {str(e)}")


@router.callback_query(F.data == "clarify_details")
async def clarify_details(callback: CallbackQuery):
    """Запрос на уточнение деталей"""
    
    clarification_text = """✏️ <b>Уточните детали задачи:</b>

Отправьте сообщение с дополнительной информацией:

📂 <b>Проект:</b> Укажите название проекта
⏰ <b>Дедлайн:</b> Когда нужно выполнить (например: "до завтра", "к пятнице")
👤 <b>Исполнитель:</b> Кому назначить задачу
⚡ <b>Приоритет:</b> Важность задачи

Пример:
"Проект: Офис, дедлайн: до пятницы, приоритет: высокий"

Или просто отправьте уточняющую информацию текстом."""
    
    await callback.message.edit_text(clarification_text)
    await callback.answer()
