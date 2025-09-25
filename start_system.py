#!/usr/bin/env python3
"""
Автоматический запуск всей системы
Запускать: python start_system.py
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Выполнение команды"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_backend():
    """Проверка backend"""
    print("🔧 Проверка backend...")
    success, stdout, stderr = run_command("python -c \"import requests; requests.get('http://127.0.0.1:8000/health')\"")
    return success

def start_backend():
    """Запуск backend"""
    print("🚀 Запуск backend...")
    
    # Проверяем, запущен ли уже
    if check_backend():
        print("✅ Backend уже запущен")
        return True
    
    # Запускаем backend в фоне
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Директория backend не найдена")
        return False
    
    # Проверяем .env
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("❌ Файл backend/.env не найден")
        return False
    
    # Запускаем backend
    if os.name == 'nt':  # Windows
        subprocess.Popen(["python", "main.py"], cwd=backend_dir, shell=True)
    else:  # Unix/Linux
        subprocess.Popen(["python", "main.py"], cwd=backend_dir)
    
    # Ждем запуска
    for i in range(10):
        time.sleep(2)
        if check_backend():
            print("✅ Backend запущен успешно")
            return True
        print(f"⏳ Ожидание запуска backend... ({i+1}/10)")
    
    print("❌ Backend не запустился")
    return False

def check_bot():
    """Проверка bot"""
    print("🤖 Проверка bot...")
    
    bot_dir = Path("bot")
    if not bot_dir.exists():
        print("❌ Директория bot не найдена")
        return False
    
    env_file = bot_dir / ".env"
    if not env_file.exists():
        print("❌ Файл bot/.env не найден")
        return False
    
    return True

def start_bot():
    """Запуск bot"""
    print("🤖 Запуск bot...")
    
    if not check_bot():
        return False
    
    bot_dir = Path("bot")
    
    # Запускаем bot в фоне
    if os.name == 'nt':  # Windows
        subprocess.Popen(["python", "main.py"], cwd=bot_dir, shell=True)
    else:  # Unix/Linux
        subprocess.Popen(["python", "main.py"], cwd=bot_dir)
    
    print("✅ Bot запущен")
    return True

def check_frontend():
    """Проверка frontend"""
    print("🌐 Проверка frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Директория frontend не найдена")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json не найден")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("❌ node_modules не найден. Запустите: cd frontend && npm install")
        return False
    
    return True

def start_frontend():
    """Запуск frontend"""
    print("🌐 Запуск frontend...")
    
    if not check_frontend():
        return False
    
    frontend_dir = Path("frontend")
    
    # Запускаем frontend в фоне
    if os.name == 'nt':  # Windows
        subprocess.Popen(["npm", "start"], cwd=frontend_dir, shell=True)
    else:  # Unix/Linux
        subprocess.Popen(["npm", "start"], cwd=frontend_dir)
    
    print("✅ Frontend запущен")
    return True

def main():
    """Главная функция"""
    print("🚀 АВТОМАТИЧЕСКИЙ ЗАПУСК СИСТЕМЫ")
    print("=" * 50)
    
    # Проверяем инициализацию
    print("🔍 Проверка инициализации...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Директория backend не найдена")
        return
    
    # Проверяем создателя
    success, stdout, stderr = run_command(
        "python -c \"import requests; r=requests.get('http://127.0.0.1:8000/api/v1/users/check-access/434532312'); print('OK' if r.status_code==200 else 'FAIL')\""
    )
    
    if not success or "FAIL" in stdout:
        print("⚠️ Создатель не инициализирован. Инициализируем...")
        success, stdout, stderr = run_command("python init_creator.py", cwd=backend_dir)
        if success:
            print("✅ Создатель инициализирован")
        else:
            print("❌ Ошибка инициализации создателя")
            print(f"Ошибка: {stderr}")
            return
    else:
        print("✅ Создатель уже инициализирован")
    
    # Запускаем компоненты
    components = [
        ("Backend", start_backend),
        ("Bot", start_bot),
        ("Frontend", start_frontend),
    ]
    
    for name, start_func in components:
        print(f"\n📦 Запуск {name}...")
        if not start_func():
            print(f"❌ Не удалось запустить {name}")
            return
        time.sleep(2)
    
    print("\n🎉 ВСЕ КОМПОНЕНТЫ ЗАПУЩЕНЫ!")
    print("=" * 50)
    print("📋 СИСТЕМА ГОТОВА К РАБОТЕ:")
    print("✅ Backend: http://127.0.0.1:8000")
    print("✅ Bot: Запущен и готов к работе")
    print("✅ Frontend: http://localhost:3000")
    
    print("\n🔍 ТЕСТИРОВАНИЕ:")
    print("1. Отправьте /start боту с ID 434532312")
    print("2. Откройте http://localhost:3000 в браузере")
    print("3. Перейдите в админ панель")
    print("4. Запустите тест: python test_access_quick.py")
    
    print("\n📱 ДОСТУП К АДМИН ПАНЕЛИ:")
    print("1. Откройте веб-приложение")
    print("2. Войдите как создатель (ID: 434532312)")
    print("3. Перейдите в раздел 'Админ панель'")
    print("4. Добавьте пользователей и управляйте системой")
    
    print("\n⚠️ Для остановки системы закройте все окна терминала")

if __name__ == "__main__":
    main()
