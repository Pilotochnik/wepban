#!/bin/bash

echo "🔧 Подготовка проекта для деплоя на сервер..."

# Обновляем конфигурацию backend для продакшена
echo "📝 Обновляем backend конфигурацию..."
sed -i 's|WEBAPP_URL: str = "http://localhost:3000"|WEBAPP_URL: str = "https://projectmanager.chickenkiller.com"|g' backend/app/core/config.py
sed -i 's|BACKEND_URL: str = "http://127.0.0.1:8000"|BACKEND_URL: str = "https://projectmanager.chickenkiller.com"|g' backend/app/core/config.py

# Обновляем конфигурацию bot для продакшена
echo "📝 Обновляем bot конфигурацию..."
sed -i 's|WEBAPP_URL: str = "http://localhost:3000"|WEBAPP_URL: str = "https://projectmanager.chickenkiller.com"|g' bot/app/core/config.py
sed -i 's|BACKEND_URL: str = "http://127.0.0.1:8000"|BACKEND_URL: str = "https://projectmanager.chickenkiller.com"|g' bot/app/core/config.py

# Обновляем frontend API для продакшена
echo "📝 Обновляем frontend конфигурацию..."
sed -i 's|const API_BASE_URL = import.meta.env.VITE_API_URL || '\''http://127.0.0.1:8000'\''|const API_BASE_URL = import.meta.env.VITE_API_URL || '\''https://projectmanager.chickenkiller.com/api'\''|g' frontend/src/lib/api.ts

# Обновляем TaskDetailModal для продакшена
echo "📝 Обновляем TaskDetailModal..."
sed -i 's|src={`http://127.0.0.1:8000/api/v1/photos/tasks/${task.id}/photo/`}|src={`https://projectmanager.chickenkiller.com/api/v1/photos/tasks/${task.id}/photo/`}|g' frontend/src/components/TaskDetailModal.tsx

# Обновляем CORS настройки в backend
echo "📝 Обновляем CORS настройки..."
sed -i 's|"http://localhost:3000",|"https://projectmanager.chickenkiller.com",|g' backend/main.py
sed -i 's|"http://127.0.0.1:3000",|"https://projectmanager.chickenkiller.com",|g' backend/main.py

echo "✅ Проект подготовлен для деплоя!"
echo "📝 Теперь выполните:"
echo "  ./upload_to_server.bat"
echo "  ssh root@194.87.76.75"
echo "  cd /var/www/project-manager"
echo "  chmod +x *.sh"
echo "  ./setup_env.sh"
echo "  ./start_all.sh"
echo "  ./setup_ssl.sh"
