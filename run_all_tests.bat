@echo off
chcp 65001 >nul
echo 🧪 Запуск всех тестов Project Manager Bot
echo ================================================

echo.
echo 📋 Проверяем зависимости...
python -c "import httpx, asyncio" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Установите зависимости: pip install httpx
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.

echo 🚀 Запуск основного тестирования...
python test_all_functions.py

echo.
echo 🔐 Запуск тестирования системы ролей...
python test_role_system.py

echo.
echo 📊 Все тесты завершены!
echo Проверьте файлы отчетов:
echo   - test_report.json
echo   - role_system_test_report.json
echo.
pause
