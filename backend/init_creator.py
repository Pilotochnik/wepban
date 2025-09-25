#!/usr/bin/env python3
"""
Скрипт для инициализации создателя в системе
Запускать: python init_creator.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.task import Task
from app.models.approval import ApprovalRequest
from app.core.database import Base

def init_creator():
    """Инициализация создателя в системе"""
    
    # Создаем таблицы
    print("🔧 Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже создатель
        creator = db.query(User).filter(User.telegram_id == 434532312).first()
        
        if creator:
            print(f"✅ Создатель уже существует: {creator.first_name} {creator.last_name}")
            print(f"   Роль: {creator.role}")
            print(f"   Активен: {creator.is_active}")
        else:
            # Создаем создателя
            print("👑 Создание создателя в системе...")
            creator = User(
                telegram_id=434532312,
                username="ttvdnl",  # Замените на реальный username
                first_name="Создатель",
                last_name="Проекта",
                role=UserRole.CREATOR,
                is_active=True
            )
            
            db.add(creator)
            db.commit()
            db.refresh(creator)
            
            print(f"✅ Создатель создан: {creator.first_name} {creator.last_name}")
            print(f"   Telegram ID: {creator.telegram_id}")
            print(f"   Роль: {creator.role}")
        
        # Создаем тестовый проект
        test_project = db.query(Project).filter(Project.name == "Тестовый проект").first()
        if not test_project:
            print("📂 Создание тестового проекта...")
            test_project = Project(
                name="Тестовый проект",
                description="Проект для тестирования системы",
                created_by=creator.id
            )
            db.add(test_project)
            db.commit()
            db.refresh(test_project)
            print(f"✅ Тестовый проект создан: {test_project.name}")
        
        # Создаем тестовую задачу
        test_task = db.query(Task).filter(Task.title == "Тестовая задача").first()
        if not test_task:
            print("📋 Создание тестовой задачи...")
            test_task = Task(
                title="Тестовая задача",
                description="Задача для тестирования системы",
                project_id=test_project.id,
                created_by=creator.id,
                priority="medium",
                status="todo"
            )
            db.add(test_task)
            db.commit()
            db.refresh(test_task)
            print(f"✅ Тестовая задача создана: {test_task.title}")
        
        print("\n🎉 Инициализация завершена!")
        print("\n📊 Статистика системы:")
        print(f"   👥 Пользователей: {db.query(User).count()}")
        print(f"   📂 Проектов: {db.query(Project).count()}")
        print(f"   📋 Задач: {db.query(Task).count()}")
        print(f"   ⏳ Запросов на одобрение: {db.query(ApprovalRequest).count()}")
        
        print("\n🔑 Данные для входа:")
        print(f"   Telegram ID создателя: {creator.telegram_id}")
        print(f"   Username: @{creator.username}")
        print(f"   Роль: {creator.role}")
        
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Инициализация системы управления проектами")
    print("=" * 50)
    init_creator()
