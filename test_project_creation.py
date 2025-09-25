#!/usr/bin/env python3
"""
Тест создания проекта с детальной диагностикой
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.user_project import UserProject, ProjectRole
from app.crud.project import project_crud
from app.schemas.project import ProjectCreate

def test_project_creation():
    """Тест создания проекта"""
    print("🔍 Тест создания проекта...")
    
    db = SessionLocal()
    
    try:
        # Получаем создателя
        creator = db.query(User).filter(User.telegram_id == 434532312).first()
        if not creator:
            print("❌ Создатель не найден")
            return False
        
        print(f"✅ Создатель найден: {creator.first_name} {creator.last_name}")
        print(f"   ID: {creator.id}")
        
        # Создаем проект
        project_data = ProjectCreate(
            name="Тестовый проект",
            description="Описание проекта"
        )
        
        print("🔧 Создание проекта...")
        try:
            project = project_crud.create(db, project_data, creator.id)
            print(f"✅ Проект создан: {project.name}")
            print(f"   ID: {project.id}")
            print(f"   Created by: {project.created_by}")
            
            # Проверяем UserProject
            user_project = db.query(UserProject).filter(
                UserProject.user_id == creator.id,
                UserProject.project_id == project.id
            ).first()
            
            if user_project:
                print(f"✅ UserProject создан: роль {user_project.role}")
            else:
                print("❌ UserProject не создан")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка создания проекта: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    test_project_creation()
