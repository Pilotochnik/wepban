@echo off
chcp 65001 >nul
echo Подготовка проекта для деплоя на сервер...

REM Обновляем конфигурацию backend для продакшена
echo Обновляем backend конфигурацию...
powershell -Command "(Get-Content 'backend/app/core/config.py') -replace 'WEBAPP_URL: str = \"http://localhost:3000\"', 'WEBAPP_URL: str = \"https://projectmanager.chickenkiller.com\"' | Set-Content 'backend/app/core/config.py'"
powershell -Command "(Get-Content 'backend/app/core/config.py') -replace 'BACKEND_URL: str = \"http://127.0.0.1:8000\"', 'BACKEND_URL: str = \"https://projectmanager.chickenkiller.com\"' | Set-Content 'backend/app/core/config.py'"

REM Обновляем конфигурацию bot для продакшена
echo Обновляем bot конфигурацию...
powershell -Command "(Get-Content 'bot/app/core/config.py') -replace 'WEBAPP_URL: str = \"http://localhost:3000\"', 'WEBAPP_URL: str = \"https://projectmanager.chickenkiller.com\"' | Set-Content 'bot/app/core/config.py'"
powershell -Command "(Get-Content 'bot/app/core/config.py') -replace 'BACKEND_URL: str = \"http://127.0.0.1:8000\"', 'BACKEND_URL: str = \"https://projectmanager.chickenkiller.com\"' | Set-Content 'bot/app/core/config.py'"

REM Обновляем frontend API для продакшена
echo Обновляем frontend конфигурацию...
powershell -Command "(Get-Content 'frontend/src/lib/api.ts') -replace 'http://127.0.0.1:8000', 'https://projectmanager.chickenkiller.com/api' | Set-Content 'frontend/src/lib/api.ts'"

REM Обновляем TaskDetailModal для продакшена
echo Обновляем TaskDetailModal...
powershell -Command "(Get-Content 'frontend/src/components/TaskDetailModal.tsx') -replace 'http://127.0.0.1:8000', 'https://projectmanager.chickenkiller.com/api' | Set-Content 'frontend/src/components/TaskDetailModal.tsx'"

REM Обновляем CORS настройки в backend
echo Обновляем CORS настройки...
powershell -Command "(Get-Content 'backend/main.py') -replace '\"http://localhost:3000\",', '\"https://projectmanager.chickenkiller.com\",' | Set-Content 'backend/main.py'"
powershell -Command "(Get-Content 'backend/main.py') -replace '\"http://127.0.0.1:3000\",', '\"https://projectmanager.chickenkiller.com\",' | Set-Content 'backend/main.py'"

echo Проект подготовлен для деплоя!
echo Теперь выполните:
echo   upload_to_server.bat
echo   ssh root@194.87.76.75
echo   cd /var/www/project-manager
echo   chmod +x *.sh
echo   ./setup_env.sh
echo   ./start_all.sh
echo   ./setup_ssl.sh
pause
