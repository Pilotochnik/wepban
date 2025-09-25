from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.services.auth import get_current_user
import os
import shutil
from pathlib import Path

router = APIRouter()

# Папка для хранения фото
PHOTOS_DIR = Path("uploads/photos")
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/tasks/{task_id}/photo/")
async def upload_task_photo(
    task_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Загрузка фото для задачи"""
    
    # Проверяем, что задача существует
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверяем права доступа (только создатель или создатель задачи)
    from app.models.user import UserRole
    if current_user.role != UserRole.CREATOR and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав для изменения этой задачи")
    
    # Проверяем тип файла
    if not photo.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")
    
    # Генерируем уникальное имя файла
    file_extension = Path(photo.filename).suffix
    filename = f"task_{task_id}_{current_user.id}{file_extension}"
    file_path = PHOTOS_DIR / filename
    
    try:
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        # Обновляем задачу (можно добавить поле photo_url в модель Task)
        # task.photo_url = str(file_path)  # Пока просто сохраняем путь
        
        print(f"Photo saved for task {task_id}: {file_path}")
        
        return {
            "message": "Фото успешно загружено",
            "task_id": task_id,
            "photo_path": str(file_path)
        }
        
    except Exception as e:
        print(f"Error saving photo: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сохранения фото")

@router.get("/tasks/{task_id}/photo/")
async def get_task_photo(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение фото задачи"""
    
    # Проверяем, что задача существует и принадлежит пользователю
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Ищем фото для задачи
    photo_pattern = f"task_{task_id}_{current_user.id}.*"
    photos = list(PHOTOS_DIR.glob(photo_pattern))
    
    if not photos:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    
    photo_path = photos[0]
    
    return {
        "task_id": task_id,
        "photo_exists": True,
        "photo_path": str(photo_path)
    }
