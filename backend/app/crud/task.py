from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.task import Task, TaskComment
from app.schemas.task import TaskCreate, TaskUpdate, TaskCommentCreate
from app.models.user import UserRole


class TaskCRUD:
    def create(self, db: Session, task: TaskCreate, created_by: int) -> Task:
        db_task = Task(**task.dict(), created_by=created_by)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get(self, db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    def get_by_user(self, db: Session, user_id: int, user_role: UserRole) -> List[Task]:
        """Получение всех задач пользователя с учетом роли"""
        if user_role == UserRole.CREATOR:
            return db.query(Task).all()
        else:
            # Пользователь видит только свои задачи или назначенные ему
            return db.query(Task).filter(
                (Task.created_by == user_id) | (Task.assigned_to == user_id)
            ).all()

    def get_by_project(self, db: Session, project_id: int, user_role: UserRole, user_id: int) -> List[Task]:
        if user_role == UserRole.CREATOR:
            return db.query(Task).filter(Task.project_id == project_id).all()
        else:
            # Пользователь видит только свои задачи или назначенные ему
            return db.query(Task).filter(
                and_(
                    Task.project_id == project_id,
                    (Task.created_by == user_id) | (Task.assigned_to == user_id)
                )
            ).all()

    def update(self, db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            update_data = task_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_task, field, value)
            db.commit()
            db.refresh(db_task)
        return db_task

    def delete(self, db: Session, task_id: int) -> bool:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
            return True
        return False

    def add_comment(self, db: Session, comment: TaskCommentCreate, task_id: int, author_id: int) -> TaskComment:
        db_comment = TaskComment(**comment.dict(), task_id=task_id, author_id=author_id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment


task_crud = TaskCRUD()
