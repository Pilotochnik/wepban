#!/usr/bin/env python3
"""
Тест для проверки enum значений
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import UserRole

print("🔍 Проверка enum UserRole:")
print(f"Доступные роли: {list(UserRole)}")

for role in UserRole:
    print(f"  - {role.name}: {role.value}")

print("\n🔍 Проверка конкретных ролей:")
try:
    print(f"CREATOR: {UserRole.CREATOR}")
    print(f"FOREMAN: {UserRole.FOREMAN}")
    print(f"WORKER: {UserRole.WORKER}")
    print(f"VIEWER: {UserRole.VIEWER}")
    print("✅ Все роли доступны")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Проверяем, есть ли ADMIN
try:
    admin_role = UserRole.ADMIN
    print(f"❌ ADMIN все еще существует: {admin_role}")
except AttributeError:
    print("✅ ADMIN больше не существует")
except Exception as e:
    print(f"❌ Другая ошибка с ADMIN: {e}")
