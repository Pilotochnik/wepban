#!/bin/bash

echo "🔧 Возврат к локальной разработке..."

# Возвращаем конфигурацию backend для локальной разработки
echo "📝 Возвращаем backend конфигурацию..."
sed -i 's|WEBAPP_URL: str = "https://194.87.76.75:3000"|WEBAPP_URL: str = "http://localhost:3000"|g' backend/app/core/config.py
sed -i 's|BACKEND_URL: str = "https://194.87.76.75:8000"|BACKEND_URL: str = "http://127.0.0.1:8000"|g' backend/app/core/config.py

# Возвращаем конфигурацию bot для локальной разработки
echo "📝 Возвращаем bot конфигурацию..."
sed -i 's|WEBAPP_URL: str = "https://194.87.76.75:3000"|WEBAPP_URL: str = "http://localhost:3000"|g' bot/app/core/config.py
sed -i 's|BACKEND_URL: str = "https://194.87.76.75:8000"|BACKEND_URL: str = "http://127.0.0.1:8000"|g' bot/app/core/config.py

# Возвращаем frontend API для локальной разработки
echo "📝 Возвращаем frontend конфигурацию..."
sed -i 's|const API_BASE_URL = import.meta.env.VITE_API_URL || '\''https://194.87.76.75:8000'\''|const API_BASE_URL = import.meta.env.VITE_API_URL || '\''http://127.0.0.1:8000'\''|g' frontend/src/lib/api.ts

# Возвращаем TaskDetailModal для локальной разработки
echo "📝 Возвращаем TaskDetailModal..."
sed -i 's|src={`https://194.87.76.75:8000/api/v1/photos/tasks/${task.id}/photo/`}|src={`http://127.0.0.1:8000/api/v1/photos/tasks/${task.id}/photo/`}|g' frontend/src/components/TaskDetailModal.tsx

# Возвращаем CORS настройки в backend
echo "📝 Возвращаем CORS настройки..."
sed -i 's|"https://194.87.76.75:3000",|"http://localhost:3000",|g' backend/main.py
sed -i 's|"https://194.87.76.75:3000",|"http://127.0.0.1:3000",|g' backend/main.py

echo "✅ Проект возвращен к локальной разработке!"
echo "📝 Теперь можете запускать локально:"
echo "  cd backend && python main.py"
echo "  cd bot && python main.py"
echo "  cd frontend && npm run dev"
