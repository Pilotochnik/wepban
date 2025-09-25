#!/usr/bin/env python3
"""
Полная проверка системы - диагностика и исправление проблем
Запускать: python check_system.py
"""

import asyncio
import httpx
import json
import os
import sys
import subprocess
from pathlib import Path

class SystemChecker:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.creator_id = 434532312
        self.issues = []
        self.fixes = []
        
    async def run_full_check(self):
        """Полная проверка системы"""
        print("🔍 ПОЛНАЯ ДИАГНОСТИКА СИСТЕМЫ")
        print("=" * 60)
        
        checks = [
            ("📁 Проверка файловой структуры", self.check_file_structure),
            ("🔧 Проверка backend", self.check_backend),
            ("👑 Проверка создателя", self.check_creator),
            ("🗄️ Проверка базы данных", self.check_database),
            ("🔐 Проверка аутентификации", self.check_auth),
            ("📱 Проверка API endpoints", self.check_api_endpoints),
            ("🤖 Проверка bot конфигурации", self.check_bot_config),
            ("🌐 Проверка frontend", self.check_frontend),
        ]
        
        for check_name, check_func in checks:
            print(f"\n{check_name}")
            print("-" * 40)
            try:
                await check_func()
                print(f"✅ {check_name}: OK")
            except Exception as e:
                print(f"❌ {check_name}: {e}")
                self.issues.append(f"{check_name}: {e}")
        
        # Предложения по исправлению
        self.suggest_fixes()
        
        return len(self.issues) == 0
    
    async def check_file_structure(self):
        """Проверка файловой структуры"""
        required_dirs = ["backend", "bot", "frontend"]
        required_files = [
            "backend/main.py",
            "backend/.env",
            "bot/main.py", 
            "bot/.env",
            "frontend/package.json",
            ".env"
        ]
        
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                raise Exception(f"Отсутствует директория: {dir_name}")
        
        for file_name in required_files:
            if not Path(file_name).exists():
                raise Exception(f"Отсутствует файл: {file_name}")
    
    async def check_backend(self):
        """Проверка backend"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.backend_url}/health")
                if response.status_code != 200:
                    raise Exception(f"Backend недоступен: {response.status_code}")
        except httpx.ConnectError:
            raise Exception("Backend не запущен. Запустите: cd backend && python main.py")
    
    async def check_creator(self):
        """Проверка создателя"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.backend_url}/api/v1/users/check-access/{self.creator_id}")
            
            if response.status_code != 200:
                raise Exception("Создатель не найден. Запустите: python backend/init_creator.py")
            
            user_data = response.json()
            if not user_data.get('is_active'):
                raise Exception("Создатель неактивен. Запустите: python backend/init_creator.py")
            
            if user_data.get('role') != 'creator':
                raise Exception("Роль создателя неправильная. Пересоздайте пользователя.")
    
    async def check_database(self):
        """Проверка базы данных"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Проверяем создателя
            response = await client.get(f"{self.backend_url}/api/v1/users/check-access/{self.creator_id}")
            if response.status_code != 200:
                raise Exception("Проблема с базой данных - создатель не найден")
            
            user_data = response.json()
            if not user_data:
                raise Exception("База данных пуста")
    
    async def check_auth(self):
        """Проверка аутентификации"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.backend_url}/api/v1/users/auth",
                json={"telegram_id": self.creator_id}
            )
            
            if response.status_code != 200:
                raise Exception(f"Ошибка аутентификации: {response.status_code}")
            
            auth_data = response.json()
            if not auth_data.get("access_token"):
                raise Exception("Токен не получен")
    
    async def check_api_endpoints(self):
        """Проверка API endpoints"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Аутентификация
            auth_response = await client.post(
                f"{self.backend_url}/api/v1/users/auth",
                json={"telegram_id": self.creator_id}
            )
            
            if auth_response.status_code != 200:
                raise Exception("Не удалось аутентифицироваться")
            
            token = auth_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Проверяем основные endpoints
            endpoints = [
                ("/api/v1/projects/", "Проекты"),
                ("/api/v1/tasks/", "Задачи"),
                ("/api/v1/admin/users", "Админ пользователи"),
                ("/api/v1/admin/stats", "Админ статистика"),
            ]
            
            for endpoint, name in endpoints:
                response = await client.get(f"{self.backend_url}{endpoint}", headers=headers)
                if response.status_code not in [200, 404]:  # 404 допустимо для пустых списков
                    raise Exception(f"Ошибка {name}: {response.status_code}")
    
    async def check_bot_config(self):
        """Проверка конфигурации бота"""
        bot_env = Path("bot/.env")
        if not bot_env.exists():
            raise Exception("Отсутствует bot/.env файл")
        
        # Проверяем содержимое .env
        with open(bot_env, 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_vars = ["BOT_TOKEN", "BACKEND_URL", "OPENAI_API_KEY"]
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=" in content and not content.split(f"{var}=")[1].split('\n')[0].strip():
                raise Exception(f"Переменная {var} не настроена в bot/.env")
    
    async def check_frontend(self):
        """Проверка frontend"""
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            raise Exception("Директория frontend не найдена")
        
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            raise Exception("package.json не найден в frontend")
        
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            raise Exception("node_modules не найден. Запустите: cd frontend && npm install")
    
    def suggest_fixes(self):
        """Предложения по исправлению проблем"""
        if not self.issues:
            print("\n🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ УСПЕШНО!")
            print("✅ Система готова к работе!")
            return
        
        print(f"\n⚠️ НАЙДЕНО ПРОБЛЕМ: {len(self.issues)}")
        print("=" * 60)
        
        for i, issue in enumerate(self.issues, 1):
            print(f"{i}. {issue}")
        
        print("\n🔧 ПРЕДЛАГАЕМЫЕ ИСПРАВЛЕНИЯ:")
        print("=" * 60)
        
        if any("Backend не запущен" in issue for issue in self.issues):
            print("1. Запустите backend:")
            print("   cd backend")
            print("   python main.py")
        
        if any("Создатель не найден" in issue or "Создатель неактивен" in issue for issue in self.issues):
            print("2. Инициализируйте создателя:")
            print("   cd backend")
            print("   python init_creator.py")
        
        if any(".env" in issue for issue in self.issues):
            print("3. Настройте .env файлы:")
            print("   - Скопируйте .env в backend/ и bot/")
            print("   - Заполните все переменные")
        
        if any("node_modules" in issue for issue in self.issues):
            print("4. Установите зависимости frontend:")
            print("   cd frontend")
            print("   npm install")
        
        if any("База данных" in issue for issue in self.issues):
            print("5. Пересоздайте базу данных:")
            print("   cd backend")
            print("   python init_creator.py")
        
        print("\n🚀 ПОСЛЕ ИСПРАВЛЕНИЯ ЗАПУСТИТЕ:")
        print("1. Backend: cd backend && python main.py")
        print("2. Bot: cd bot && python main.py")
        print("3. Frontend: cd frontend && npm start")
        print("4. Тест: python test_access_quick.py")

async def main():
    """Главная функция"""
    checker = SystemChecker()
    
    print("🔍 Запуск полной диагностики системы...")
    print("Это займет несколько секунд...\n")
    
    success = await checker.run_full_check()
    
    if success:
        print("\n🎉 СИСТЕМА ПОЛНОСТЬЮ ГОТОВА!")
        print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. Запустите все компоненты:")
        print("   - Backend: cd backend && python main.py")
        print("   - Bot: cd bot && python main.py") 
        print("   - Frontend: cd frontend && npm start")
        print("2. Отправьте /start боту с ID 434532312")
        print("3. Откройте веб-приложение и админ панель")
        print("4. Запустите полный тест: python test_role_system.py")
    else:
        print("\n⚠️ ТРЕБУЮТСЯ ИСПРАВЛЕНИЯ!")
        print("Следуйте инструкциям выше для решения проблем.")

if __name__ == "__main__":
    asyncio.run(main())
