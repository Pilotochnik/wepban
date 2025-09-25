from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"      # Ожидает одобрения
    APPROVED = "approved"    # Одобрено
    REJECTED = "rejected"    # Отклонено

class ActionType(str, enum.Enum):
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    CREATE_PROJECT = "create_project"
    UPDATE_PROJECT = "update_project"
    DELETE_PROJECT = "delete_project"
    ADD_USER_TO_PROJECT = "add_user_to_project"
    REMOVE_USER_FROM_PROJECT = "remove_user_from_project"

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Кто выполнил действие
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requester = relationship("User", foreign_keys=[requester_id], back_populates="requests_made")
    
    # Кто должен одобрить
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approver = relationship("User", foreign_keys=[approver_id], back_populates="requests_to_approve")
    
    # Детали действия
    action_type = Column(Enum(ActionType), nullable=False)
    entity_type = Column(String(50), nullable=False)  # "task", "project", "user"
    entity_id = Column(Integer, nullable=False)
    
    # Данные для одобрения
    action_data = Column(Text)  # JSON строка с данными действия
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)
    review_comment = Column(Text)
    
    # Связь с проектом (если применимо)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="approval_requests")
