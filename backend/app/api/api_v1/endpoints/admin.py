from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth import get_current_user
from app.models.user import User, UserRole
from app.models.approval import ApprovalRequest, ApprovalStatus
from app.crud.user import user_crud
from app.crud.approval import approval_crud
from app.schemas.user import UserCreate, UserResponse
from app.schemas.approval import ApprovalResponse, ApprovalReview

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение всех пользователей (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    return user_crud.get_all(db)

@router.post("/users", response_model=UserResponse)
def add_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Добавление нового пользователя (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Проверяем, что пользователь не существует
    existing_user = user_crud.get_by_telegram_id(db, user_data.telegram_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    return user_crud.create(db, user_data)

@router.get("/approvals/pending", response_model=List[ApprovalResponse])
def get_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение запросов на одобрение (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    return approval_crud.get_pending_by_approver(db, current_user.id)

@router.post("/approvals/{approval_id}/review")
def review_approval(
    approval_id: int,
    review_data: ApprovalReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Одобрение или отклонение запроса (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    approval = approval_crud.get(db, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    if approval.approver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав для одобрения этого запроса")
    
    return approval_crud.review(db, approval_id, review_data.status, review_data.comment)

@router.patch("/users/{user_id}/status")
def toggle_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Активация/деактивация пользователя (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Нельзя деактивировать создателя
    if user.role == UserRole.CREATOR:
        raise HTTPException(status_code=400, detail="Нельзя деактивировать создателя")
    
    return user_crud.update_status(db, user_id, is_active)

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение статистики для админ панели (только для создателя)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    return {
        "total_users": user_crud.count(db),
        "active_users": user_crud.count_active(db),
        "pending_approvals": approval_crud.count_pending(db, current_user.id),
        "foremen_count": user_crud.count_by_role(db, UserRole.FOREMAN),
        "workers_count": user_crud.count_by_role(db, UserRole.WORKER)
    }
