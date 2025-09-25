#!/usr/bin/env python3
"""
Детальная отладка инициализации
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("1. Импорт базовых модулей...")
    from sqlalchemy.orm import Session
    from app.core.database import SessionLocal, engine
    print("✅ SQLAlchemy импортирован")
    
    print("2. Импорт моделей...")
    from app.models.user import User, UserRole
    print("✅ User и UserRole импортированы")
    
    from app.models.project import Project
    print("✅ Project импортирован")
    
    from app.models.task import Task
    print("✅ Task импортирован")
    
    from app.models.approval import ApprovalRequest
    print("✅ ApprovalRequest импортирован")
    
    from app.core.database import Base
    print("✅ Base импортирован")
    
    print("3. Проверка enum значений...")
    print(f"   CREATOR: {UserRole.CREATOR}")
    print(f"   FOREMAN: {UserRole.FOREMAN}")
    print(f"   WORKER: {UserRole.WORKER}")
    print(f"   VIEWER: {UserRole.VIEWER}")
    
    print("4. Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
    
    print("5. Создание сессии базы данных...")
    db = SessionLocal()
    print("✅ Сессия создана")
    
    print("6. Проверка существующего создателя...")
    creator = db.query(User).filter(User.telegram_id == 434532312).first()
    
    if creator:
        print(f"✅ Создатель найден: {creator.first_name} {creator.last_name}")
        print(f"   Роль: {creator.role}")
        print(f"   Активен: {creator.is_active}")
    else:
        print("7. Создание нового создателя...")
        creator = User(
            telegram_id=434532312,
            username="ttvdnl",
            first_name="Создатель",
            last_name="Проекта",
            role=UserRole.CREATOR,
            is_active=True
        )
        print("✅ Объект создателя создан")
        
        print("8. Добавление в базу данных...")
        db.add(creator)
        print("✅ Добавлен в сессию")
        
        print("9. Коммит изменений...")
        db.commit()
        print("✅ Коммит выполнен")
        
        db.refresh(creator)
        print("✅ Создатель создан и сохранен")
    
    print("\n🎉 ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    import traceback
    print("\n📋 Детальная информация об ошибке:")
    traceback.print_exc()
    
    # Дополнительная диагностика
    print("\n🔍 Дополнительная диагностика:")
    try:
        print(f"   Тип ошибки: {type(e).__name__}")
        print(f"   Сообщение: {str(e)}")
        
        # Проверяем, есть ли ADMIN в enum
        if hasattr(UserRole, 'ADMIN'):
            print("   ❌ ADMIN все еще существует в enum!")
        else:
            print("   ✅ ADMIN не существует в enum")
            
    except Exception as diag_e:
        print(f"   Ошибка диагностики: {diag_e}")
    
finally:
    try:
        db.close()
        print("\n🔒 Сессия базы данных закрыта")
    except:
        pass
