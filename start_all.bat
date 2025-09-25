@echo off
echo ========================================
echo    Запуск Project Manager System
echo ========================================

echo.
echo 1. Запуск Backend...
start "Backend" cmd /k "cd backend && .\venv\Scripts\Activate.ps1 && python main.py"

echo.
echo 2. Запуск Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo 3. Запуск Telegram Bot...
start "Bot" cmd /k "cd bot && .\venv\Scripts\Activate.ps1 && python main.py"

echo.
echo ========================================
echo    Все компоненты запущены!
echo ========================================
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo Bot: @wwwpan_bot
echo.
echo Для тестирования:
echo - python setup_web_panel.py
echo - python test_bot.py
echo.
pause
