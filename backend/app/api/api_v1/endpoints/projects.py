from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.crud.project import project_crud
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()


@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание нового проекта"""
    print(f"Creating project: {project.name} for user: {current_user.id}")
    return project_crud.create(db=db, project=project, owner_id=current_user.id)


@router.get("/", response_model=List[Project])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка проектов пользователя"""
    return project_crud.get_user_projects(db=db, user_id=current_user.id, user_role=current_user.role)


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение проекта по ID"""
    project = project_crud.get(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Проверка доступа к проекту
    user_projects = project_crud.get_user_projects(db=db, user_id=current_user.id, user_role=current_user.role)
    if project not in user_projects:
        raise HTTPException(status_code=403, detail="Нет доступа к этому проекту")
    
    return project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление проекта"""
    project = project_crud.get(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Проверка доступа к проекту
    user_projects = project_crud.get_user_projects(db=db, user_id=current_user.id, user_role=current_user.role)
    if project not in user_projects:
        raise HTTPException(status_code=403, detail="Нет доступа к этому проекту")
    
    return project_crud.update(db=db, project_id=project_id, project_update=project_update)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление проекта"""
    project = project_crud.get(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Проверка доступа к проекту
    user_projects = project_crud.get_user_projects(db=db, user_id=current_user.id, user_role=current_user.role)
    if project not in user_projects:
        raise HTTPException(status_code=403, detail="Нет доступа к этому проекту")
    
    success = project_crud.delete(db=db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=400, detail="Не удалось удалить проект")
    
    return {"message": "Проект удален"}
