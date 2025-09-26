#!/usr/bin/env python3
"""
Скрипт для добавления прораба в тестовый проект
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.user_project import UserProject, ProjectRole

def add_foreman_to_project():
    """Добавление прораба в тестовый проект"""
    
    db = SessionLocal()
    
    try:
        # Находим тестовый проект
        test_project = db.query(Project).filter(Project.name == "Тестовый проект").first()
        if not test_project:
            print("❌ Тестовый проект не найден")
            return
        
        print(f"📂 Найден проект: {test_project.name} (ID: {test_project.id})")
        
        # Находим или создаем прораба
        foreman = db.query(User).filter(User.telegram_id == 123456789).first()  # Замените на реальный ID прораба
        
        if not foreman:
            print("👷 Создание тестового прораба...")
            foreman = User(
                telegram_id=123456789,  # Замените на реальный Telegram ID
                username="test_foreman",
                first_name="Тестовый",
                last_name="Прораб",
                role=UserRole.FOREMAN,
                is_active=True
            )
            db.add(foreman)
            db.commit()
            db.refresh(foreman)
            print(f"✅ Прораб создан: {foreman.first_name} {foreman.last_name}")
        else:
            print(f"👷 Найден прораб: {foreman.first_name} {foreman.last_name}")
        
        # Проверяем, не добавлен ли уже прораб в проект
        existing = db.query(UserProject).filter(
            UserProject.user_id == foreman.id,
            UserProject.project_id == test_project.id
        ).first()
        
        if existing:
            print("⚠️ Прораб уже добавлен в этот проект")
        else:
            # Добавляем прораба в проект
            user_project = UserProject(
                user_id=foreman.id,
                project_id=test_project.id,
                role=ProjectRole.MEMBER
            )
            db.add(user_project)
            db.commit()
            print(f"✅ Прораб {foreman.first_name} {foreman.last_name} добавлен в проект {test_project.name}")
        
        # Показываем статистику
        print(f"\n📊 Статистика проекта {test_project.name}:")
        project_users = db.query(UserProject).filter(UserProject.project_id == test_project.id).all()
        for pu in project_users:
            user = db.query(User).filter(User.id == pu.user_id).first()
            print(f"   👤 {user.first_name} {user.last_name} ({user.role}) - {pu.role}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Добавление прораба в тестовый проект")
    print("=" * 50)
    print("⚠️ ВАЖНО: Замените telegram_id=123456789 на реальный ID прораба!")
    print("=" * 50)
    add_foreman_to_project()
