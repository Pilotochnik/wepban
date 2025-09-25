from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.approval import ApprovalStatus, ActionType
from app.schemas.user import UserResponse

class ApprovalBase(BaseModel):
    action_type: ActionType
    entity_type: str
    entity_id: int
    action_data: Optional[str] = None
    project_id: Optional[int] = None

class ApprovalCreate(ApprovalBase):
    requester_id: int
    approver_id: int

class ApprovalUpdate(BaseModel):
    status: ApprovalStatus
    review_comment: Optional[str] = None

class ApprovalReview(BaseModel):
    status: ApprovalStatus
    comment: Optional[str] = None

class ApprovalResponse(ApprovalBase):
    id: int
    requester_id: int
    approver_id: int
    requester: UserResponse
    approver: UserResponse
    status: ApprovalStatus
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    review_comment: Optional[str] = None
    
    class Config:
        from_attributes = True
