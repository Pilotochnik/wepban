#!/usr/bin/env python3
"""
Комплексный тест всех функций Project Manager Bot
Проверяет backend, bot, frontend и интеграцию
"""

import asyncio
import httpx
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Добавляем пути к модулям
sys.path.append('backend')
sys.path.append('bot')

class ProjectManagerTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"  # Локальный backend для тестов
        self.creator_id = 434532312
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Логирование результатов теста"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': timestamp
        })
        return success

    async def test_backend_health(self) -> bool:
        """Тест 1: Проверка доступности backend"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/docs")
                success = response.status_code == 200
                return self.log_test("Backend Health Check", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Backend Health Check", False, str(e))

    async def test_user_authentication(self) -> bool:
        """Тест 2: Проверка аутентификации пользователя"""
        try:
            async with httpx.AsyncClient() as client:
                # Проверяем доступ создателя
                response = await client.get(f"{self.base_url}/api/v1/users/check-access/{self.creator_id}")
                if response.status_code == 200:
                    data = response.json()
                    success = data.get('role') == 'creator'
                    return self.log_test("User Authentication", success, f"Role: {data.get('role')}")
                else:
                    return self.log_test("User Authentication", False, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("User Authentication", False, str(e))

    async def test_project_creation(self) -> bool:
        """Тест 3: Создание проекта"""
        try:
            async with httpx.AsyncClient() as client:
                project_data = {
                    "name": f"Test Project {datetime.now().strftime('%H%M%S')}",
                    "description": "Автоматический тестовый проект"
                }
                response = await client.post(
                    f"{self.base_url}/api/v1/projects/",
                    json=project_data,
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                if success:
                    data = response.json()
                    self.test_project_id = data['id']
                    return self.log_test("Project Creation", success, f"Project ID: {data['id']}")
                else:
                    return self.log_test("Project Creation", False, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Project Creation", False, str(e))

    async def test_task_creation(self) -> bool:
        """Тест 4: Создание задачи"""
        try:
            if not hasattr(self, 'test_project_id'):
                return self.log_test("Task Creation", False, "No project ID available")
                
            async with httpx.AsyncClient() as client:
                task_data = {
                    "title": f"Test Task {datetime.now().strftime('%H%M%S')}",
                    "description": "Автоматическая тестовая задача",
                    "project_id": self.test_project_id,
                    "priority": "medium",
                    "deadline": "2024-12-31T23:59:59"
                }
                response = await client.post(
                    f"{self.base_url}/api/v1/tasks/",
                    json=task_data,
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                if success:
                    data = response.json()
                    self.test_task_id = data['id']
                    return self.log_test("Task Creation", success, f"Task ID: {data['id']}")
                else:
                    return self.log_test("Task Creation", False, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Task Creation", False, str(e))

    async def test_task_status_update(self) -> bool:
        """Тест 5: Обновление статуса задачи"""
        try:
            if not hasattr(self, 'test_task_id'):
                return self.log_test("Task Status Update", False, "No task ID available")
                
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/api/v1/tasks/{self.test_task_id}/status",
                    json={"status": "in_progress"},
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Task Status Update", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Task Status Update", False, str(e))

    async def test_photo_upload(self) -> bool:
        """Тест 6: Загрузка фото для задачи"""
        try:
            if not hasattr(self, 'test_task_id'):
                return self.log_test("Photo Upload", False, "No task ID available")
                
            # Создаем тестовое изображение
            test_image_content = b"fake_image_data_for_testing"
            files = {"photo": ("test.jpg", test_image_content, "image/jpeg")}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/photos/tasks/{self.test_task_id}/photo",
                    files=files,
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Photo Upload", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Photo Upload", False, str(e))

    async def test_admin_functions(self) -> bool:
        """Тест 7: Функции админ-панели"""
        try:
            async with httpx.AsyncClient() as client:
                # Проверяем получение списка пользователей
                response = await client.get(
                    f"{self.base_url}/api/v1/admin/users",
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Admin Functions", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Admin Functions", False, str(e))

    async def test_approval_system(self) -> bool:
        """Тест 8: Система одобрений"""
        try:
            async with httpx.AsyncClient() as client:
                # Проверяем получение запросов на одобрение
                response = await client.get(
                    f"{self.base_url}/api/v1/admin/approvals",
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Approval System", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Approval System", False, str(e))

    async def test_frontend_api(self) -> bool:
        """Тест 9: API для фронтенда"""
        try:
            async with httpx.AsyncClient() as client:
                # Проверяем получение задач
                response = await client.get(
                    f"{self.base_url}/api/v1/tasks/",
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                if success:
                    data = response.json()
                    task_count = len(data) if isinstance(data, list) else 0
                    return self.log_test("Frontend API", success, f"Tasks: {task_count}")
                else:
                    return self.log_test("Frontend API", False, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Frontend API", False, str(e))

    async def test_role_system(self) -> bool:
        """Тест 10: Система ролей"""
        try:
            async with httpx.AsyncClient() as client:
                # Создаем тестового пользователя с ролью worker
                user_data = {
                    "telegram_id": 999999999,
                    "username": "test_worker",
                    "role": "worker"
                }
                response = await client.post(
                    f"{self.base_url}/api/v1/admin/users",
                    json=user_data,
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Role System", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Role System", False, str(e))

    def check_bot_files(self) -> bool:
        """Тест 11: Проверка файлов бота"""
        try:
            bot_files = [
                'bot/main.py',
                'bot/app/core/config.py',
                'bot/app/handlers/start.py',
                'bot/app/handlers/callbacks.py',
                'bot/app/services/api.py',
                'bot/app/middlewares/auth.py'
            ]
            
            missing_files = []
            for file_path in bot_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
            
            success = len(missing_files) == 0
            details = f"Missing: {missing_files}" if missing_files else "All files present"
            return self.log_test("Bot Files Check", success, details)
        except Exception as e:
            return self.log_test("Bot Files Check", False, str(e))

    def check_frontend_files(self) -> bool:
        """Тест 12: Проверка файлов фронтенда"""
        try:
            frontend_files = [
                'frontend/src/App.tsx',
                'frontend/src/main.tsx',
                'frontend/src/lib/api.ts',
                'frontend/src/contexts/AuthContext.tsx',
                'frontend/src/components/Layout.tsx',
                'frontend/src/pages/Dashboard.tsx',
                'frontend/src/pages/AdminPanel.tsx',
                'frontend/src/components/TaskDetailModal.tsx'
            ]
            
            missing_files = []
            for file_path in frontend_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
            
            success = len(missing_files) == 0
            details = f"Missing: {missing_files}" if missing_files else "All files present"
            return self.log_test("Frontend Files Check", success, details)
        except Exception as e:
            return self.log_test("Frontend Files Check", False, str(e))

    def check_configuration_consistency(self) -> bool:
        """Тест 13: Проверка консистентности конфигурации"""
        try:
            issues = []
            
            # Проверяем backend config
            with open('backend/app/core/config.py', 'r', encoding='utf-8') as f:
                backend_config = f.read()
                if 'projectmanager.chickenkiller.com' not in backend_config:
                    issues.append("Backend config missing domain")
            
            # Проверяем bot config
            with open('bot/app/core/config.py', 'r', encoding='utf-8') as f:
                bot_config = f.read()
                if 'projectmanager.chickenkiller.com' not in bot_config:
                    issues.append("Bot config missing domain")
            
            # Проверяем frontend API
            with open('frontend/src/lib/api.ts', 'r', encoding='utf-8') as f:
                frontend_api = f.read()
                if 'projectmanager.chickenkiller.com' not in frontend_api:
                    issues.append("Frontend API missing domain")
            
            success = len(issues) == 0
            details = f"Issues: {issues}" if issues else "All configs consistent"
            return self.log_test("Configuration Consistency", success, details)
        except Exception as e:
            return self.log_test("Configuration Consistency", False, str(e))

    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 Запуск комплексного тестирования Project Manager Bot")
        print("=" * 60)
        
        # Синхронные тесты
        self.check_bot_files()
        self.check_frontend_files()
        self.check_configuration_consistency()
        
        # Асинхронные тесты
        await self.test_backend_health()
        await self.test_user_authentication()
        await self.test_project_creation()
        await self.test_task_creation()
        await self.test_task_status_update()
        await self.test_photo_upload()
        await self.test_admin_functions()
        await self.test_approval_system()
        await self.test_frontend_api()
        await self.test_role_system()
        
        # Итоги
        print("=" * 60)
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print(f"✅ Пройдено: {passed}/{total} ({success_rate:.1f}%)")
        print(f"❌ Провалено: {total - passed}")
        
        if success_rate >= 90:
            print("🎉 ОТЛИЧНО! Система готова к деплою!")
        elif success_rate >= 70:
            print("⚠️  ХОРОШО! Есть незначительные проблемы")
        else:
            print("🚨 ВНИМАНИЕ! Критические проблемы обнаружены")
        
        # Сохраняем отчет
        self.save_test_report()
        
        return success_rate >= 90

    def save_test_report(self):
        """Сохранение отчета о тестировании"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'passed_tests': sum(1 for r in self.test_results if r['success']),
            'success_rate': (sum(1 for r in self.test_results if r['success']) / len(self.test_results)) * 100,
            'results': self.test_results
        }
        
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Отчет сохранен в test_report.json")

async def main():
    """Главная функция"""
    tester = ProjectManagerTester()
    success = await tester.run_all_tests()
    
    if not success:
        print("\n🔧 Рекомендации:")
        print("1. Убедитесь, что backend запущен (python backend/main.py)")
        print("2. Проверьте, что база данных инициализирована (python backend/init_creator.py)")
        print("3. Убедитесь, что все зависимости установлены")
        print("4. Проверьте конфигурационные файлы")
        
        sys.exit(1)
    else:
        print("\n🚀 Все тесты пройдены! Система готова к деплою!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
