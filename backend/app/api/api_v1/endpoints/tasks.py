from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth import get_current_user
from app.models.user import User, UserRole
from app.models.approval import ApprovalRequest, ActionType, ApprovalStatus
from app.crud.task import task_crud
from app.crud.approval import approval_crud
from app.crud.user import user_crud
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskComment, TaskCommentCreate
from app.schemas.approval import ApprovalCreate
from app.services.notifications import notification_service
import json

router = APIRouter()


@router.get("/", response_model=List[Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение всех задач пользователя"""
    return task_crud.get_by_user(db=db, user_id=current_user.id, user_role=current_user.role)


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение конкретной задачи"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверяем права доступа
    if current_user.role != UserRole.CREATOR and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    return task


@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание новой задачи"""
    try:
        print(f"Creating task: {task.dict()}")
        print(f"Current user: {current_user.id}, role: {current_user.role}")
        
        # Проверяем права пользователя
        if current_user.role not in [UserRole.CREATOR, UserRole.FOREMAN]:
            raise HTTPException(status_code=403, detail="Недостаточно прав для создания задач")
        
        # Если создатель - создаем сразу
        if current_user.role == UserRole.CREATOR:
            print("Creating task as CREATOR")
            result = task_crud.create(db=db, task=task, created_by=current_user.id)
            print(f"Task created successfully: {result.id}")
            return result
    except Exception as e:
        print(f"Error in create_task: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
    # Если прораб - создаем запрос на одобрение
    creator = user_crud.get_by_telegram_id(db, 434532312)  # ID создателя
    if not creator:
        raise HTTPException(status_code=500, detail="Создатель не найден в системе")
    
    # Создаем запрос на одобрение
    approval_data = ApprovalCreate(
        requester_id=current_user.id,
        approver_id=creator.id,
        action_type=ActionType.CREATE_TASK,
        entity_type="task",
        entity_id=0,  # Будет обновлен после создания задачи
        action_data=json.dumps({
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "project_id": task.project_id
        }),
        project_id=task.project_id
    )
    
    approval = approval_crud.create(db, approval_data)
    
    # Отправляем уведомление создателю
    await notification_service.notify_approval_request(creator, approval)
    
    raise HTTPException(
        status_code=202, 
        detail="Задача отправлена на одобрение создателю"
    )


@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление задачи"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверяем права доступа
    if current_user.role != UserRole.CREATOR and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    return task_crud.update(db=db, task_id=task_id, task_update=task_update)


@router.get("/project/{project_id}", response_model=List[Task])
def get_tasks_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение задач по проекту"""
    return task_crud.get_by_project(
        db=db, 
        project_id=project_id, 
        user_role=current_user.role,
        user_id=current_user.id
    )


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение задачи по ID"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверка прав доступа
    if (current_user.role != UserRole.CREATOR and
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление задачи"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверка прав доступа
    if (current_user.role != UserRole.CREATOR and
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    return task_crud.update(db=db, task_id=task_id, task_update=task_update)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление задачи"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Только создатель или админ может удалить задачу
    if current_user.role != UserRole.CREATOR and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление задачи")
    
    success = task_crud.delete(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Не удалось удалить задачу")
    
    return {"message": "Задача удалена"}


@router.post("/{task_id}/comments", response_model=TaskComment)
def add_comment(
    task_id: int,
    comment: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Добавление комментария к задаче"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверка прав доступа
    if (current_user.role != UserRole.CREATOR and
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    return task_crud.add_comment(db=db, comment=comment, task_id=task_id, author_id=current_user.id)


@router.post("/{task_id}/attachments")
def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Загрузка файла к задаче"""
    task = task_crud.get(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверка прав доступа
    if (current_user.role != UserRole.CREATOR and
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа к этой задаче")
    
    # Здесь должна быть логика сохранения файла
    # Для примера возвращаем успех
    return {"message": "Файл загружен", "filename": file.filename}
