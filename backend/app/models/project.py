from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    color = Column(String, default="#3B82F6", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("UserProject", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    approval_requests = relationship("ApprovalRequest", back_populates="project")
