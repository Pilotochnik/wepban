from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = "#3B82F6"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class Project(ProjectBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
