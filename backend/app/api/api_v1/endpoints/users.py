from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth import get_current_user, create_access_token
from app.models.user import User, UserRole
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, AuthRequest
from app.crud.user import user_crud

router = APIRouter()


@router.post("/register", response_model=UserSchema)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    # Проверяем, не существует ли уже пользователь с таким telegram_id
    existing_user = user_crud.get_by_telegram_id(db=db, telegram_id=user.telegram_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким Telegram ID уже существует")
    
    return user_crud.create(db=db, user=user)


@router.post("/auth")
def authenticate_user(
    request: AuthRequest,
    db: Session = Depends(get_db)
):
    """Аутентификация пользователя через Telegram ID"""
    telegram_id = request.telegram_id
    print(f"Auth request for telegram_id: {telegram_id}")
    
    if not telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id обязателен")
    
    user = user_crud.get_by_telegram_id(db=db, telegram_id=telegram_id)
    if not user:
        print(f"User not found for telegram_id: {telegram_id}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if not user.is_active:
        print(f"User {telegram_id} is not active")
        raise HTTPException(status_code=400, detail="Пользователь деактивирован")
    
    access_token = create_access_token(telegram_id=telegram_id)
    print(f"Token created for user {telegram_id}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/check-access/{telegram_id}")
def check_user_access(
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Проверка доступа пользователя к боту"""
    try:
        print(f"Checking access for telegram_id: {telegram_id}")
        user = user_crud.get_by_telegram_id(db, telegram_id)
        print(f"User found: {user}")
        
        if not user:
            print("User not found")
            return {"is_active": False, "message": "Пользователь не найден"}
        
        result = {
            "is_active": user.is_active,
            "role": user.role.value if user.role else None,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }
        print(f"Returning result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in check_user_access: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return current_user


@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление информации о текущем пользователе"""
    return user_crud.update(db=db, user_id=current_user.id, user_update=user_update)


@router.get("/", response_model=List[UserSchema])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка пользователей (только для админов)"""
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    return user_crud.get_all(db=db)
