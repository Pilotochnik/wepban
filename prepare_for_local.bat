@echo off
echo 🔧 Возврат к локальной разработке...

REM Возвращаем конфигурацию backend для локальной разработки
echo 📝 Возвращаем backend конфигурацию...
powershell -Command "(Get-Content 'backend/app/core/config.py') -replace 'WEBAPP_URL: str = \"https://194.87.76.75:3000\"', 'WEBAPP_URL: str = \"http://localhost:3000\"' | Set-Content 'backend/app/core/config.py'"
powershell -Command "(Get-Content 'backend/app/core/config.py') -replace 'BACKEND_URL: str = \"https://194.87.76.75:8000\"', 'BACKEND_URL: str = \"http://127.0.0.1:8000\"' | Set-Content 'backend/app/core/config.py'"

REM Возвращаем конфигурацию bot для локальной разработки
echo 📝 Возвращаем bot конфигурацию...
powershell -Command "(Get-Content 'bot/app/core/config.py') -replace 'WEBAPP_URL: str = \"https://194.87.76.75:3000\"', 'WEBAPP_URL: str = \"http://localhost:3000\"' | Set-Content 'bot/app/core/config.py'"
powershell -Command "(Get-Content 'bot/app/core/config.py') -replace 'BACKEND_URL: str = \"https://194.87.76.75:8000\"', 'BACKEND_URL: str = \"http://127.0.0.1:8000\"' | Set-Content 'bot/app/core/config.py'"

REM Возвращаем frontend API для локальной разработки
echo 📝 Возвращаем frontend конфигурацию...
powershell -Command "(Get-Content 'frontend/src/lib/api.ts') -replace 'https://194.87.76.75:8000', 'http://127.0.0.1:8000' | Set-Content 'frontend/src/lib/api.ts'"

REM Возвращаем TaskDetailModal для локальной разработки
echo 📝 Возвращаем TaskDetailModal...
powershell -Command "(Get-Content 'frontend/src/components/TaskDetailModal.tsx') -replace 'https://194.87.76.75:8000', 'http://127.0.0.1:8000' | Set-Content 'frontend/src/components/TaskDetailModal.tsx'"

REM Возвращаем CORS настройки в backend
echo 📝 Возвращаем CORS настройки...
powershell -Command "(Get-Content 'backend/main.py') -replace '\"https://194.87.76.75:3000\",', '\"http://localhost:3000\",' | Set-Content 'backend/main.py'"
powershell -Command "(Get-Content 'backend/main.py') -replace '\"https://194.87.76.75:3000\",', '\"http://127.0.0.1:3000\",' | Set-Content 'backend/main.py'"

echo ✅ Проект возвращен к локальной разработке!
echo 📝 Теперь можете запускать локально:
echo   cd backend && python main.py
echo   cd bot && python main.py
echo   cd frontend && npm run dev
pause
