from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import tempfile
import os
from app.services.api import APIService

router = Router()


@router.message(F.content_type == "photo")
async def handle_photo(message: Message):
    """Обработка фотографий"""
    
    # Показываем, что бот обрабатывает фото
    processing_msg = await message.answer("📸 Обрабатываю фотографию...")
    
    try:
        # Получаем самое большое фото
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        
        # Сохраняем во временный файл
        temp_file_path = tempfile.mktemp(suffix=".jpg")
        print(f"PHOTO HANDLER: Скачиваем файл в: {temp_file_path}")
        
        try:
            # В Aiogram 3.x используем bot.download_file
            await message.bot.download_file(file.file_path, temp_file_path)
            print(f"PHOTO HANDLER: Файл успешно скачан: {temp_file_path}")
            
            # Проверяем, что файл существует и не пустой
            if os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
                print(f"PHOTO HANDLER: Размер файла: {os.path.getsize(temp_file_path)} байт")
            else:
                print("PHOTO HANDLER: ОШИБКА - файл не существует или пустой!")
                await processing_msg.edit_text("❌ Ошибка загрузки фотографии")
                return
                
        except Exception as e:
            print(f"PHOTO HANDLER: Ошибка скачивания файла: {e}")
            await processing_msg.edit_text("❌ Ошибка загрузки фотографии")
            return
        
        # Получаем проекты пользователя для выбора
        api_service = APIService()
        projects = await api_service.get_user_projects(message.from_user.id)
        
        if not projects:
            # Нет проектов - предлагаем создать
            text = "📸 <b>Фото получено!</b>\n\n"
            text += "У вас пока нет проектов. Создайте проект в веб-приложении, чтобы прикрепить фото к задаче."
            
            # Временно убираем WebApp кнопку из-за HTTPS требований
            # keyboard = InlineKeyboardMarkup(inline_keyboard=[
            #     [InlineKeyboardButton(text="🚀 Открыть веб-приложение", web_app={"url": f"{api_service.WEBAPP_URL}"})]
            # ])
            
            await processing_msg.edit_text(text)
            return
        
        # Показываем проекты для выбора
        text = "📸 <b>Фото получено!</b>\n\n"
        text += "Выберите проект, к которому создать задачу с фото:"
        
        # Сохраняем путь к фото в глобальной переменной или используем другой способ
        # В реальном приложении лучше сохранять в базу данных или кэш
        import hashlib
        photo_hash = hashlib.md5(temp_file_path.encode()).hexdigest()
        
        # Сохраняем маппинг hash -> path (в реальном приложении используйте Redis или БД)
        if not hasattr(create_task_with_photo, 'photo_cache'):
            create_task_with_photo.photo_cache = {}
        create_task_with_photo.photo_cache[photo_hash] = temp_file_path
        
        keyboard_buttons = []
        for project in projects:
            # Используем hash вместо полного пути
            callback_data = f"create_task_with_photo:{project['id']}:{photo_hash}"
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=f"📂 {project['name']}", 
                    callback_data=callback_data
                )
            ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await processing_msg.edit_text(text, reply_markup=keyboard)
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка обработки фотографии: {str(e)}")
    
    finally:
        # Удаляем временный файл
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.callback_query(F.data.startswith("create_task_with_photo:"))
async def create_task_with_photo(callback: CallbackQuery):
    """Создание задачи с фото"""
    
    # Извлекаем project_id и photo_hash из callback_data
    parts = callback.data.split(":")
    project_id = int(parts[1])
    photo_hash = parts[2] if len(parts) > 2 else None
    
    # Получаем путь к фото из кэша
    photo_path = None
    if photo_hash and hasattr(create_task_with_photo, 'photo_cache'):
        photo_path = create_task_with_photo.photo_cache.get(photo_hash)
        print(f"Retrieved photo path: {photo_path}")
    
    await callback.answer("⏳ Создаю задачу с фото...")
    
    try:
        api_service = APIService()
        
        # Получаем информацию о проекте
        projects = await api_service.get_user_projects(callback.from_user.id)
        project = next((p for p in projects if p["id"] == project_id), None)
        
        if not project:
            await callback.message.edit_text("❌ Проект не найден")
            return
        
        # Создаем задачу с фото
        task_data = {
            "title": f"Задача с фото в проекте {project['name']}",
            "description": f"Задача создана из фото, отправленного в Telegram. Проект: {project['name']}",
            "project_id": project_id,
            "priority": "medium",
            "deadline": None
        }
        
        created_task = await api_service.create_task(task_data, callback.from_user.id)
        
        if created_task:
            # Пытаемся сохранить фото для задачи
            photo_saved = False
            if photo_path and os.path.exists(photo_path):
                photo_saved = await api_service.save_photo_for_task(
                    callback.from_user.id, 
                    photo_path, 
                    created_task['id']
                )
                print(f"Photo saved: {photo_saved}")
            
            success_text = f"✅ <b>Задача создана с фото!</b>\n\n"
            success_text += f"📋 <b>Название:</b> {created_task['title']}\n"
            success_text += f"📝 <b>Описание:</b> {created_task['description']}\n"
            success_text += f"📂 <b>Проект:</b> {project['name']}\n"
            success_text += f"📸 <b>Фото:</b> {'Прикреплено' if photo_saved else 'Не удалось прикрепить'}\n"
            success_text += f"⚡ <b>Приоритет:</b> {created_task['priority']}\n"
            success_text += f"🆔 <b>ID задачи:</b> {created_task['id']}\n\n"
            success_text += f"Задача появится в веб-приложении!"
            
            await callback.message.edit_text(success_text)
            
            # Удаляем временный файл и очищаем кэш
            if photo_path and os.path.exists(photo_path):
                os.unlink(photo_path)
            
            # Очищаем кэш
            if photo_hash and hasattr(create_task_with_photo, 'photo_cache'):
                create_task_with_photo.photo_cache.pop(photo_hash, None)
        else:
            await callback.message.edit_text("❌ Не удалось создать задачу")
    
    except Exception as e:
        print(f"PHOTO CALLBACK ERROR: {e}")
        await callback.message.edit_text(f"❌ Ошибка создания задачи: {str(e)}")


