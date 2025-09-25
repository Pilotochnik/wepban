from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ProjectRole(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"
    VIEWER = "viewer"


class UserProject(Base):
    __tablename__ = "user_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(Enum(ProjectRole), default=ProjectRole.MEMBER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="users")
