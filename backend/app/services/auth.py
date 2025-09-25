from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from typing import Optional

security = HTTPBearer()


def verify_telegram_auth(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Проверка Telegram WebApp авторизации"""
    print(f"Verifying token: {credentials.credentials[:20]}...")
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telegram_id: int = payload.get("sub")
        print(f"Decoded telegram_id: {telegram_id}")
        if telegram_id is None:
            print("No telegram_id in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен авторизации",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"telegram_id": telegram_id}
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    auth_data: dict = Depends(verify_telegram_auth),
    db: Session = Depends(get_db)
) -> User:
    """Получение текущего пользователя"""
    user = db.query(User).filter(User.telegram_id == auth_data["telegram_id"]).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь деактивирован"
        )
    return user


def create_access_token(telegram_id: int) -> str:
    """Создание JWT токена"""
    to_encode = {"sub": str(telegram_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
