#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram Bot
Тестирует создание задач из текстовых и голосовых сообщений
"""

import asyncio
import httpx
import json
from typing import Dict, List

class BotTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.telegram_id = 434532312
        
    async def authenticate(self) -> str:
        """Аутентификация пользователя"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/users/auth",
                json={"telegram_id": self.telegram_id}
            )
            response.raise_for_status()
            data = response.json()
            return data["access_token"]
    
    async def get_projects(self, token: str) -> List[Dict]:
        """Получение проектов пользователя"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(
                f"{self.base_url}/api/v1/projects/",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_project(self, token: str, name: str, description: str = "", color: str = "#3B82F6") -> Dict:
        """Создание проекта"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"{self.base_url}/api/v1/projects/",
                headers=headers,
                json={
                    "name": name,
                    "description": description,
                    "color": color
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def create_task(self, token: str, task_data: Dict) -> Dict:
        """Создание задачи"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"{self.base_url}/api/v1/tasks/",
                headers=headers,
                json=task_data
            )
            response.raise_for_status()
            return response.json()
    
    async def test_text_tasks(self, token: str, projects: List[Dict]):
        """Тестирование создания задач из текстовых сообщений"""
        print("\n🧪 Тестирование текстовых задач:")
        
        test_messages = [
            "создай задачу: купить молоко",
            "добавь задачу: позвонить клиенту",
            "задача: подготовить презентацию",
            "создай задачу: помыть посуду",
            "добавить задачу: записаться к врачу"
        ]
        
        for message in test_messages:
            print(f"\n📝 Тестируем: '{message}'")
            
            # Симулируем AI анализ
            task_data = {
                "title": message.split(":")[-1].strip().title(),
                "description": f"Задача создана из сообщения: {message}",
                "project_id": projects[0]["id"] if projects else None,
                "priority": "medium",
                "deadline": None
            }
            
            try:
                created_task = await self.create_task(token, task_data)
                print(f"✅ Задача создана: {created_task['title']} (ID: {created_task['id']})")
            except Exception as e:
                print(f"❌ Ошибка создания задачи: {e}")
    
    async def test_voice_tasks(self, token: str, projects: List[Dict]):
        """Тестирование создания задач из голосовых сообщений"""
        print("\n🎤 Тестирование голосовых задач:")
        
        voice_scenarios = [
            {
                "transcribed_text": "Создай задачу купить корм для кота",
                "expected_task": "Купить корм для кота"
            },
            {
                "transcribed_text": "Добавь задачу убраться в комнате",
                "expected_task": "Убраться в комнате"
            },
            {
                "transcribed_text": "Задача записаться на курсы",
                "expected_task": "Записаться на курсы"
            }
        ]
        
        for scenario in voice_scenarios:
            print(f"\n🎙️ Симулируем голосовое: '{scenario['transcribed_text']}'")
            
            task_data = {
                "title": scenario["expected_task"],
                "description": f"Задача создана из голосового сообщения: {scenario['transcribed_text']}",
                "project_id": projects[1]["id"] if len(projects) > 1 else None,
                "priority": "medium",
                "deadline": None
            }
            
            try:
                created_task = await self.create_task(token, task_data)
                print(f"✅ Задача создана: {created_task['title']} (ID: {created_task['id']})")
            except Exception as e:
                print(f"❌ Ошибка создания задачи: {e}")
    
    async def test_project_logic(self, token: str):
        """Тестирование логики распределения задач по проектам"""
        print("\n🏗️ Тестирование логики проектов:")
        
        # Создаем тестовые проекты
        projects_data = [
            {"name": "Домашние дела", "description": "Задачи по дому", "color": "#10B981"},
            {"name": "Работа", "description": "Рабочие задачи", "color": "#3B82F6"},
            {"name": "Личные дела", "description": "Личные задачи", "color": "#F59E0B"}
        ]
        
        created_projects = []
        for project_data in projects_data:
            try:
                project = await self.create_project(token, **project_data)
                created_projects.append(project)
                print(f"✅ Проект создан: {project['name']} (ID: {project['id']})")
            except Exception as e:
                print(f"❌ Ошибка создания проекта: {e}")
        
        return created_projects
    
    async def test_smart_project_assignment(self, token: str, projects: List[Dict]):
        """Тестирование умного распределения задач по проектам"""
        print("\n🧠 Тестирование умного распределения задач:")
        
        # Логика распределения задач по проектам
        project_keywords = {
            "Домашние дела": ["дом", "убрать", "помыть", "почистить", "приготовить", "посуда", "полы"],
            "Работа": ["работа", "клиент", "проект", "встреча", "презентация", "отчет", "звонок"],
            "Личные дела": ["врач", "курсы", "спорт", "магазин", "покупка", "личное"]
        }
        
        test_tasks = [
            "создай задачу: помыть посуду",
            "добавь задачу: позвонить клиенту",
            "задача: записаться к врачу",
            "создай задачу: убраться в комнате",
            "добавить задачу: подготовить презентацию"
        ]
        
        for task_text in test_tasks:
            # Определяем подходящий проект
            assigned_project = None
            task_content = task_text.lower()
            
            for project_name, keywords in project_keywords.items():
                if any(keyword in task_content for keyword in keywords):
                    assigned_project = next(
                        (p for p in projects if p["name"] == project_name), 
                        None
                    )
                    break
            
            if not assigned_project:
                assigned_project = projects[0]  # По умолчанию первый проект
            
            task_data = {
                "title": task_text.split(":")[-1].strip().title(),
                "description": f"Задача создана из: {task_text}",
                "project_id": assigned_project["id"],
                "priority": "medium",
                "deadline": None
            }
            
            try:
                created_task = await self.create_task(token, task_data)
                print(f"✅ Задача '{created_task['title']}' → Проект '{assigned_project['name']}'")
            except Exception as e:
                print(f"❌ Ошибка создания задачи: {e}")
    
    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 Запуск тестирования Telegram Bot")
        print("=" * 50)
        
        try:
            # Аутентификация
            print("🔑 Аутентификация...")
            token = await self.authenticate()
            print("✅ Аутентификация успешна")
            
            # Получение существующих проектов
            print("\n📋 Получение проектов...")
            existing_projects = await self.get_projects(token)
            print(f"✅ Найдено проектов: {len(existing_projects)}")
            
            # Создание тестовых проектов
            print("\n🏗️ Создание тестовых проектов...")
            test_projects = await self.test_project_logic(token)
            
            # Объединяем существующие и новые проекты
            all_projects = existing_projects + test_projects
            print(f"📊 Всего проектов: {len(all_projects)}")
            
            # Тестирование текстовых задач
            await self.test_text_tasks(token, all_projects)
            
            # Тестирование голосовых задач
            await self.test_voice_tasks(token, all_projects)
            
            # Тестирование умного распределения
            await self.test_smart_project_assignment(token, all_projects)
            
            print("\n🎉 Все тесты завершены!")
            
        except Exception as e:
            print(f"❌ Ошибка выполнения тестов: {e}")
            import traceback
            traceback.print_exc()

async def main():
    tester = BotTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
