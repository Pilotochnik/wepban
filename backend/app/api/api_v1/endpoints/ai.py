from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
import tempfile
import os
from app.core.database import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.services.ai import generate_task_from_audio, analyze_task_request
from app.crud.project import project_crud
from app.crud.task import task_crud
from app.schemas.task import TaskCreate

router = APIRouter()


@router.post("/process-audio")
async def process_audio_message(
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Обработка голосового сообщения для создания задачи"""
    
    # Сохраняем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
        content = await audio_file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Получаем проекты пользователя
        user_projects = project_crud.get_user_projects(
            db=db, 
            user_id=current_user.id, 
            user_role=current_user.role
        )
        projects_info = [{"id": p.id, "name": p.name} for p in user_projects]
        
        # Обрабатываем аудио через AI
        task_data = await generate_task_from_audio(temp_file_path, projects_info)
        
        # Если есть уточняющие вопросы, возвращаем их
        if task_data.get("questions"):
            return {
                "status": "questions_needed",
                "original_text": task_data.get("original_text"),
                "questions": task_data["questions"],
                "suggested_task": {
                    "title": task_data.get("title"),
                    "description": task_data.get("description"),
                    "priority": task_data.get("priority")
                }
            }
        
        # Создаем задачу
        task_create = TaskCreate(
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data["priority"],
            project_id=task_data.get("project_id"),
            deadline=task_data.get("deadline")
        )
        
        task = task_crud.create(db=db, task=task_create, created_by=current_user.id)
        
        return {
            "status": "task_created",
            "task": task,
            "original_text": task_data.get("original_text")
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обработки аудио: {str(e)}")
    
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/create-task-from-text")
async def create_task_from_text(
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Создание задачи из текста через AI"""
    
    try:
        # Извлекаем данные из запроса
        text = request.get("text", "")
        user_projects = request.get("user_projects", [])
        
        # Анализируем текст
        task_data = await analyze_task_request(text, user_projects)
        
        # Если есть уточняющие вопросы, возвращаем их
        if task_data.get("questions"):
            return {
                "status": "questions_needed",
                "questions": task_data["questions"],
                "suggested_task": {
                    "title": task_data.get("title"),
                    "description": task_data.get("description"),
                    "priority": task_data.get("priority")
                }
            }
        
        # Создаем задачу
        task_create = TaskCreate(
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data["priority"],
            project_id=task_data.get("project_id"),
            deadline=task_data.get("deadline")
        )
        
        task = task_crud.create(db=db, task=task_create, created_by=current_user.id)
        
        return {
            "status": "task_created",
            "task": task
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка анализа текста: {str(e)}")


@router.post("/upload-image-to-task/{task_id}")
async def upload_image_to_task(
    task_id: int,
    image_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Загрузка изображения к задаче"""
    
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверка прав доступа
    if (current_user.role != "creator" and 
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    # Здесь должна быть логика сохранения изображения
    # Для примера возвращаем успех
    return {
        "message": "Изображение загружено",
        "filename": image_file.filename,
        "task_id": task_id
    }
