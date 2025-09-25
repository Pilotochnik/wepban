from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    project_id: int
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None


class Task(TaskBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskCommentBase(BaseModel):
    content: str


class TaskCommentCreate(TaskCommentBase):
    pass


class TaskComment(TaskCommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
