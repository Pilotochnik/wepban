#!/usr/bin/env python3
"""
Быстрый тест доступа к системе
Запускать: python test_access_quick.py
"""

import asyncio
import httpx
import json

async def test_access():
    """Быстрая проверка доступа"""
    print("🔍 БЫСТРАЯ ПРОВЕРКА ДОСТУПА К СИСТЕМЕ")
    print("=" * 50)
    
    backend_url = "http://127.0.0.1:8000"
    creator_id = 434532312
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 1. Проверяем доступность backend
            print("1. 🔧 Проверка доступности backend...")
            health_response = await client.get(f"{backend_url}/health")
            if health_response.status_code == 200:
                print("   ✅ Backend доступен")
            else:
                print(f"   ❌ Backend недоступен: {health_response.status_code}")
                return False
            
            # 2. Проверяем создателя
            print("2. 👑 Проверка создателя...")
            access_response = await client.get(f"{backend_url}/api/v1/users/check-access/{creator_id}")
            
            if access_response.status_code == 200:
                user_data = access_response.json()
                print(f"   ✅ Создатель найден: {user_data.get('first_name')} {user_data.get('last_name')}")
                print(f"   📋 Роль: {user_data.get('role')}")
                print(f"   🟢 Активен: {user_data.get('is_active')}")
                
                if not user_data.get('is_active'):
                    print("   ⚠️ Создатель неактивен! Запустите: python backend/init_creator.py")
                    return False
            else:
                print(f"   ❌ Создатель не найден: {access_response.status_code}")
                print("   ⚠️ Запустите: python backend/init_creator.py")
                return False
            
            # 3. Тестируем аутентификацию
            print("3. 🔐 Тест аутентификации...")
            auth_response = await client.post(
                f"{backend_url}/api/v1/users/auth",
                json={"telegram_id": creator_id}
            )
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                token = auth_data.get("access_token")
                print("   ✅ Аутентификация успешна")
                print(f"   🎫 Токен получен: {token[:20]}...")
                
                # 4. Тестируем API с токеном
                print("4. 📊 Тест API с токеном...")
                headers = {"Authorization": f"Bearer {token}"}
                
                # Получаем проекты
                projects_response = await client.get(
                    f"{backend_url}/api/v1/projects/",
                    headers=headers
                )
                
                if projects_response.status_code == 200:
                    projects = projects_response.json()
                    print(f"   ✅ Проекты получены: {len(projects)} шт.")
                else:
                    print(f"   ❌ Ошибка получения проектов: {projects_response.status_code}")
                
                # Получаем задачи
                tasks_response = await client.get(
                    f"{backend_url}/api/v1/tasks/",
                    headers=headers
                )
                
                if tasks_response.status_code == 200:
                    tasks = tasks_response.json()
                    print(f"   ✅ Задачи получены: {len(tasks)} шт.")
                else:
                    print(f"   ❌ Ошибка получения задач: {tasks_response.status_code}")
                
                # Тестируем админ API
                print("5. 👑 Тест админ API...")
                admin_stats_response = await client.get(
                    f"{backend_url}/api/v1/admin/stats",
                    headers=headers
                )
                
                if admin_stats_response.status_code == 200:
                    stats = admin_stats_response.json()
                    print("   ✅ Админ API работает")
                    print(f"   📊 Пользователей: {stats.get('total_users', 0)}")
                    print(f"   🟢 Активных: {stats.get('active_users', 0)}")
                else:
                    print(f"   ❌ Ошибка админ API: {admin_stats_response.status_code}")
                
            else:
                print(f"   ❌ Ошибка аутентификации: {auth_response.status_code}")
                print(f"   📄 Ответ: {auth_response.text}")
                return False
            
            print("\n🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ УСПЕШНО!")
            print("✅ Система готова к работе!")
            print("\n📋 Следующие шаги:")
            print("1. Запустите бота: cd bot && python main.py")
            print("2. Отправьте /start боту с ID 434532312")
            print("3. Запустите frontend: cd frontend && npm start")
            print("4. Откройте админ панель в веб-приложении")
            
            return True
            
        except httpx.ConnectError:
            print("❌ Не удается подключиться к backend!")
            print("💡 Убедитесь, что backend запущен:")
            print("   cd backend && python main.py")
            return False
            
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False

async def main():
    """Главная функция"""
    success = await test_access()
    
    if not success:
        print("\n🔧 ВОЗМОЖНЫЕ РЕШЕНИЯ:")
        print("1. Запустите backend: cd backend && python main.py")
        print("2. Инициализируйте создателя: cd backend && python init_creator.py")
        print("3. Проверьте .env файлы")
        print("4. Проверьте логи backend")

if __name__ == "__main__":
    asyncio.run(main())
