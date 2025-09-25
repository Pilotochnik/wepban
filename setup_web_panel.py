#!/usr/bin/env python3
"""
Скрипт для настройки веб-панели
Создает тестовые проекты и настраивает систему
"""

import asyncio
import httpx
import json

class WebPanelSetup:
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
    
    async def create_default_projects(self, token: str):
        """Создание стандартных проектов"""
        print("🏗️ Создание стандартных проектов...")
        
        default_projects = [
            {
                "name": "Домашние дела",
                "description": "Задачи по дому и быту",
                "color": "#10B981"
            },
            {
                "name": "Работа",
                "description": "Рабочие задачи и проекты",
                "color": "#3B82F6"
            },
            {
                "name": "Личные дела",
                "description": "Личные задачи и планы",
                "color": "#F59E0B"
            },
            {
                "name": "Здоровье",
                "description": "Задачи связанные со здоровьем",
                "color": "#EF4444"
            },
            {
                "name": "Обучение",
                "description": "Задачи по обучению и развитию",
                "color": "#8B5CF6"
            }
        ]
        
        created_projects = []
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            for project_data in default_projects:
                try:
                    response = await client.post(
                        f"{self.base_url}/api/v1/projects/",
                        headers=headers,
                        json=project_data
                    )
                    response.raise_for_status()
                    project = response.json()
                    created_projects.append(project)
                    print(f"✅ Проект создан: {project['name']} (ID: {project['id']})")
                except Exception as e:
                    print(f"❌ Ошибка создания проекта '{project_data['name']}': {e}")
        
        return created_projects
    
    async def create_sample_tasks(self, token: str, projects: list):
        """Создание примеров задач"""
        print("\n📝 Создание примеров задач...")
        
        sample_tasks = [
            {
                "title": "Помыть посуду",
                "description": "Помыть всю накопившуюся посуду",
                "project_id": projects[0]["id"],  # Домашние дела
                "priority": "medium",
                "status": "todo"
            },
            {
                "title": "Подготовить презентацию",
                "description": "Подготовить презентацию для клиента",
                "project_id": projects[1]["id"],  # Работа
                "priority": "high",
                "status": "in_progress"
            },
            {
                "title": "Записаться к врачу",
                "description": "Записаться на прием к терапевту",
                "project_id": projects[3]["id"],  # Здоровье
                "priority": "high",
                "status": "todo"
            },
            {
                "title": "Изучить Python",
                "description": "Пройти курс по Python программированию",
                "project_id": projects[4]["id"],  # Обучение
                "priority": "medium",
                "status": "todo"
            },
            {
                "title": "Купить продукты",
                "description": "Сходить в магазин за продуктами",
                "project_id": projects[2]["id"],  # Личные дела
                "priority": "low",
                "status": "done"
            }
        ]
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            for task_data in sample_tasks:
                try:
                    response = await client.post(
                        f"{self.base_url}/api/v1/tasks/",
                        headers=headers,
                        json=task_data
                    )
                    response.raise_for_status()
                    task = response.json()
                    project_name = next(p["name"] for p in projects if p["id"] == task_data["project_id"])
                    print(f"✅ Задача создана: '{task['title']}' → Проект '{project_name}'")
                except Exception as e:
                    print(f"❌ Ошибка создания задачи '{task_data['title']}': {e}")
    
    async def get_system_stats(self, token: str):
        """Получение статистики системы"""
        print("\n📊 Статистика системы:")
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            # Получение проектов
            try:
                response = await client.get(f"{self.base_url}/api/v1/projects/", headers=headers)
                response.raise_for_status()
                projects = response.json()
                print(f"📁 Проектов: {len(projects)}")
                
                for project in projects:
                    print(f"   - {project['name']} (ID: {project['id']})")
                    
            except Exception as e:
                print(f"❌ Ошибка получения проектов: {e}")
    
    async def setup(self):
        """Основная настройка системы"""
        print("🚀 Настройка веб-панели Project Manager")
        print("=" * 50)
        
        try:
            # Аутентификация
            print("🔑 Аутентификация...")
            token = await self.authenticate()
            print("✅ Аутентификация успешна")
            
            # Создание проектов
            projects = await self.create_default_projects(token)
            
            # Создание примеров задач
            await self.create_sample_tasks(token, projects)
            
            # Статистика
            await self.get_system_stats(token)
            
            print("\n🎉 Настройка завершена!")
            print("\n📋 Следующие шаги:")
            print("1. Откройте http://localhost:3000 в браузере")
            print("2. Перейдите в раздел 'Проекты'")
            print("3. Проверьте созданные проекты и задачи")
            print("4. Протестируйте создание новых задач")
            print("5. Запустите test_bot.py для тестирования bot'а")
            
        except Exception as e:
            print(f"❌ Ошибка настройки: {e}")
            import traceback
            traceback.print_exc()

async def main():
    setup = WebPanelSetup()
    await setup.setup()

if __name__ == "__main__":
    asyncio.run(main())
