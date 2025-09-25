from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD:
    def create(self, db: Session, user: UserCreate) -> User:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_telegram_id(self, db: Session, telegram_id: int) -> Optional[User]:
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def get_all(self, db: Session) -> List[User]:
        return db.query(User).all()

    def count(self, db: Session) -> int:
        return db.query(User).count()

    def count_active(self, db: Session) -> int:
        return db.query(User).filter(User.is_active == True).count()

    def count_by_role(self, db: Session, role) -> int:
        return db.query(User).filter(User.role == role).count()

    def update_status(self, db: Session, user_id: int, is_active: bool) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.is_active = is_active
            db.commit()
            db.refresh(db_user)
        return db_user

    def update(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    def delete(self, db: Session, user_id: int) -> bool:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False


user_crud = UserCRUD()
