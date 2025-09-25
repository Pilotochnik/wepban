#!/usr/bin/env python3
"""
Реальный тест Telegram Bot
Проверяет, что bot действительно работает и создает задачи
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List

class RealBotTester:
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
    
    async def get_projects(self) -> List[Dict]:
        """Получение проектов пользователя"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await client.get(
                f"{self.base_url}/api/v1/projects/",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_tasks(self) -> List[Dict]:
        """Получение задач пользователя"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await client.get(
                f"{self.base_url}/api/v1/tasks/",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    
    async def count_tasks_before(self) -> int:
        """Подсчет задач до тестирования"""
        tasks = await self.get_tasks()
        return len(tasks)
    
    async def wait_for_new_task(self, initial_count: int, timeout: int = 30) -> bool:
        """Ожидание появления новой задачи"""
        print(f"⏳ Ожидаем появления новой задачи (таймаут: {timeout}с)...")
        
        for i in range(timeout):
            await asyncio.sleep(1)
            try:
                current_count = len(await self.get_tasks())
                if current_count > initial_count:
                    print(f"✅ Новая задача обнаружена! Было: {initial_count}, стало: {current_count}")
                    return True
            except Exception as e:
                print(f"❌ Ошибка при проверке задач: {e}")
            
            if i % 5 == 0 and i > 0:
                print(f"⏳ Прошло {i} секунд...")
        
        print(f"❌ Таймаут! Новая задача не появилась за {timeout} секунд")
        return False
    
    async def test_bot_commands(self):
        """Тестирование команд bot'а"""
        print("\n🤖 Тестирование команд bot'а:")
        print("=" * 50)
        
        # Аутентификация
        print("🔑 Аутентификация...")
        await self.authenticate()
        print("✅ Аутентификация успешна")
        
        # Получение текущего состояния
        print("\n📊 Текущее состояние системы:")
        projects = await self.get_projects()
        tasks = await self.get_tasks()
        print(f"📁 Проектов: {len(projects)}")
        print(f"📝 Задач: {len(tasks)}")
        
        if projects:
            print("\n📋 Доступные проекты:")
            for project in projects:
                print(f"   - {project['name']} (ID: {project['id']})")
        
        print("\n🧪 Инструкции для тестирования:")
        print("=" * 50)
        print("1. Откройте Telegram и найдите вашего bot'а")
        print("2. Отправьте команду /start")
        print("3. Отправьте текстовое сообщение:")
        print("   'создай задачу: купить молоко'")
        print("4. Подождите ответа bot'а")
        print("5. Нажмите Enter для проверки результата...")
        
        # Подсчет задач до тестирования
        initial_task_count = await self.count_tasks_before()
        print(f"\n📊 Задач до тестирования: {initial_task_count}")
        
        # Ожидание ввода пользователя
        input("\n⏸️  Нажмите Enter после отправки сообщения bot'у...")
        
        # Проверка появления новой задачи
        new_task_appeared = await self.wait_for_new_task(initial_task_count, 30)
        
        if new_task_appeared:
            print("\n🎉 Тест успешен!")
            print("✅ Bot успешно создал задачу")
            
            # Показываем новые задачи
            final_tasks = await self.get_tasks()
            new_tasks = final_tasks[initial_task_count:]
            
            print(f"\n📝 Созданные задачи:")
            for task in new_tasks:
                project_name = "Без проекта"
                if task.get("project_id"):
                    project = next((p for p in projects if p["id"] == task["project_id"]), None)
                    if project:
                        project_name = project["name"]
                
                print(f"   - {task['title']} → {project_name}")
        else:
            print("\n❌ Тест не прошел!")
            print("❌ Bot не создал задачу")
            
            # Проверяем логи bot'а
            print("\n🔍 Возможные проблемы:")
            print("1. Bot не запущен")
            print("2. Bot не обрабатывает сообщения")
            print("3. Ошибка в AI сервисе")
            print("4. Проблема с API")
    
    async def test_ai_service(self):
        """Тестирование AI сервиса напрямую"""
        print("\n🧠 Тестирование AI сервиса:")
        print("=" * 50)
        
        async with httpx.AsyncClient() as client:
            try:
                # Тест AI анализа текста
                test_text = "создай задачу: купить молоко"
                projects = await self.get_projects()
                
                response = await client.post(
                    f"{self.base_url}/api/v1/ai/create-task-from-text/",
                    json={
                        "text": test_text,
                        "user_projects": projects
                    }
                )
                
                if response.status_code == 200:
                    ai_result = response.json()
                    print(f"✅ AI анализ успешен:")
                    print(f"   Текст: {test_text}")
                    print(f"   Результат: {ai_result}")
                else:
                    print(f"❌ AI анализ не удался: {response.status_code}")
                    print(f"   Ответ: {response.text}")
                    
            except Exception as e:
                print(f"❌ Ошибка AI сервиса: {e}")

async def main():
    tester = RealBotTester()
    
    print("🚀 Реальный тест Telegram Bot")
    print("=" * 50)
    
    try:
        # Тестирование AI сервиса
        await tester.test_ai_service()
        
        # Тестирование bot'а
        await tester.test_bot_commands()
        
    except Exception as e:
        print(f"❌ Ошибка выполнения тестов: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
