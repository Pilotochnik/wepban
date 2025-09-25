from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.project import Project
from app.models.user_project import UserProject, ProjectRole
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.user import UserRole


class ProjectCRUD:
    def create(self, db: Session, project: ProjectCreate, owner_id: int) -> Project:
        project_data = project.dict()
        project_data['created_by'] = owner_id
        db_project = Project(**project_data)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Добавляем создателя как владельца проекта
        user_project = UserProject(
            user_id=owner_id,
            project_id=db_project.id,
            role=ProjectRole.OWNER
        )
        db.add(user_project)
        db.commit()
        
        return db_project

    def get(self, db: Session, project_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()

    def get_user_projects(self, db: Session, user_id: int, user_role: UserRole) -> List[Project]:
        if user_role == UserRole.CREATOR:
            return db.query(Project).filter(Project.is_active == True).all()
        else:
            return db.query(Project).join(UserProject).filter(
                and_(
                    UserProject.user_id == user_id,
                    Project.is_active == True
                )
            ).all()

    def update(self, db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            update_data = project_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_project, field, value)
            db.commit()
            db.refresh(db_project)
        return db_project

    def delete(self, db: Session, project_id: int) -> bool:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db_project.is_active = False
            db.commit()
            return True
        return False

    def add_user(self, db: Session, project_id: int, user_id: int, role: ProjectRole = ProjectRole.MEMBER) -> UserProject:
        user_project = UserProject(
            user_id=user_id,
            project_id=project_id,
            role=role
        )
        db.add(user_project)
        db.commit()
        db.refresh(user_project)
        return user_project


project_crud = ProjectCRUD()
