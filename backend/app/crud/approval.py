from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.approval import ApprovalRequest, ApprovalStatus, ActionType
from app.models.user import User
from app.schemas.approval import ApprovalCreate, ApprovalUpdate
from datetime import datetime

class ApprovalCRUD:
    def create(self, db: Session, approval: ApprovalCreate) -> ApprovalRequest:
        """Создание запроса на одобрение"""
        db_approval = ApprovalRequest(**approval.dict())
        db.add(db_approval)
        db.commit()
        db.refresh(db_approval)
        return db_approval

    def get(self, db: Session, approval_id: int) -> Optional[ApprovalRequest]:
        """Получение запроса по ID"""
        return db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()

    def get_pending_by_approver(self, db: Session, approver_id: int) -> List[ApprovalRequest]:
        """Получение всех ожидающих одобрения запросов для конкретного одобряющего"""
        return db.query(ApprovalRequest).filter(
            ApprovalRequest.approver_id == approver_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).order_by(ApprovalRequest.created_at.desc()).all()

    def get_by_requester(self, db: Session, requester_id: int) -> List[ApprovalRequest]:
        """Получение всех запросов конкретного пользователя"""
        return db.query(ApprovalRequest).filter(
            ApprovalRequest.requester_id == requester_id
        ).order_by(ApprovalRequest.created_at.desc()).all()

    def review(self, db: Session, approval_id: int, status: ApprovalStatus, comment: Optional[str] = None) -> ApprovalRequest:
        """Одобрение или отклонение запроса"""
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            return None
        
        approval.status = status
        approval.reviewed_at = datetime.utcnow()
        approval.review_comment = comment
        
        db.commit()
        db.refresh(approval)
        return approval

    def count_pending(self, db: Session, approver_id: int) -> int:
        """Подсчет ожидающих одобрения запросов"""
        return db.query(ApprovalRequest).filter(
            ApprovalRequest.approver_id == approver_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).count()

    def get_by_entity(self, db: Session, entity_type: str, entity_id: int) -> List[ApprovalRequest]:
        """Получение запросов по сущности"""
        return db.query(ApprovalRequest).filter(
            ApprovalRequest.entity_type == entity_type,
            ApprovalRequest.entity_id == entity_id
        ).all()

    def delete(self, db: Session, approval_id: int) -> bool:
        """Удаление запроса"""
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            return False
        
        db.delete(approval)
        db.commit()
        return True

    def get_pending_by_project(self, db: Session, project_id: int) -> List[ApprovalRequest]:
        """Получение ожидающих запросов по проекту"""
        return db.query(ApprovalRequest).filter(
            ApprovalRequest.project_id == project_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).all()

approval_crud = ApprovalCRUD()
