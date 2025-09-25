from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    CREATOR = "creator"      # Создатель проекта (ID: 434532312)
    FOREMAN = "foreman"      # Прораб
    WORKER = "worker"        # Рабочий
    VIEWER = "viewer"        # Только просмотр


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.WORKER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("UserProject", back_populates="user")
    created_tasks = relationship("Task", foreign_keys="Task.created_by", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    comments = relationship("TaskComment", back_populates="author")
    
    # Approval relationships
    requests_made = relationship("ApprovalRequest", foreign_keys="ApprovalRequest.requester_id", back_populates="requester")
    requests_to_approve = relationship("ApprovalRequest", foreign_keys="ApprovalRequest.approver_id", back_populates="approver")
