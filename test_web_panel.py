#!/usr/bin/env python3
"""
Тест веб-панели
Проверяет, что веб-панель может получить проекты и создать новые
"""

import asyncio
import httpx
import json

class WebPanelTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.telegram_id = 434532312
        self.token = None
        
    async def authenticate(self) -> str:
        """Аутентификация пользователя"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/users/auth",
                json={"telegram_id": self.telegram_id}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            return self.token
    
    async def test_projects_api(self):
        """Тестирование API проектов"""
        print("🧪 Тестирование API проектов:")
        print("=" * 50)
        
        # Аутентификация
        print("🔑 Аутентификация...")
        await self.authenticate()
        print(f"✅ Токен получен: {self.token[:20]}...")
        
        # Получение проектов
        print("\n📋 Получение проектов...")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await client.get(f"{self.base_url}/api/v1/projects/", headers=headers)
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Проектов получено: {len(projects)}")
                for project in projects:
                    print(f"   - {project['name']} (ID: {project['id']})")
            else:
                print(f"❌ Ошибка получения проектов: {response.status_code}")
                print(f"   Ответ: {response.text}")
        
        # Создание нового проекта
        print("\n➕ Создание нового проекта...")
        new_project = {
            "name": "Тестовый проект из веб-панели",
            "description": "Проект создан для тестирования веб-панели",
            "color": "#FF6B6B"
        }
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await client.post(
                f"{self.base_url}/api/v1/projects/",
                headers=headers,
                json=new_project
            )
            
            if response.status_code == 200:
                created_project = response.json()
                print(f"✅ Проект создан: {created_project['name']} (ID: {created_project['id']})")
            else:
                print(f"❌ Ошибка создания проекта: {response.status_code}")
                print(f"   Ответ: {response.text}")
        
        # Получение задач
        print("\n📝 Получение задач...")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await client.get(f"{self.base_url}/api/v1/tasks/", headers=headers)
            
            if response.status_code == 200:
                tasks = response.json()
                print(f"✅ Задач получено: {len(tasks)}")
                for task in tasks[:5]:  # Показываем только первые 5
                    print(f"   - {task['title']} (ID: {task['id']})")
            else:
                print(f"❌ Ошибка получения задач: {response.status_code}")
                print(f"   Ответ: {response.text}")
    
    async def test_cors(self):
        """Тестирование CORS для веб-панели"""
        print("\n🌐 Тестирование CORS:")
        print("=" * 50)
        
        async with httpx.AsyncClient() as client:
            # Тест OPTIONS запроса
            response = await client.options(f"{self.base_url}/api/v1/projects/")
            print(f"OPTIONS запрос: {response.status_code}")
            
            # Проверяем заголовки CORS
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("access-control-allow-origin"),
                "Access-Control-Allow-Methods": response.headers.get("access-control-allow-methods"),
                "Access-Control-Allow-Headers": response.headers.get("access-control-allow-headers"),
            }
            
            print("CORS заголовки:")
            for header, value in cors_headers.items():
                print(f"   {header}: {value}")

async def main():
    tester = WebPanelTester()
    
    print("🚀 Тест веб-панели Project Manager")
    print("=" * 50)
    
    try:
        await tester.test_projects_api()
        await tester.test_cors()
        
        print("\n🎉 Тест завершен!")
        print("\n📋 Результаты:")
        print("1. Если все тесты прошли успешно - проблема в frontend")
        print("2. Если есть ошибки API - проблема в backend")
        print("3. Проверьте консоль браузера на http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Ошибка выполнения тестов: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
