#!/bin/bash
echo "🚀 Запуск всех сервисов Project Manager..."

# Переходим в папку проекта
cd /var/www/project-manager

# Останавливаем старые процессы
echo "🛑 Остановка старых процессов..."
pkill -f "python main.py" 2>/dev/null
pkill -f "npm run preview" 2>/dev/null
pkill -f "vite preview" 2>/dev/null
sleep 3

# Создаем папку для логов
mkdir -p logs

# Устанавливаем недостающие зависимости
echo "📦 Проверка зависимостей..."
cd bot && source venv/bin/activate && pip install pydantic-settings "pydantic>=2.4.1,<2.6" >/dev/null 2>&1 && cd ..
cd backend && source venv/bin/activate && pip install pydantic-settings >/dev/null 2>&1 && cd ..

# Запускаем backend
echo "🔧 Запуск backend..."
cd backend
source venv/bin/activate
nohup python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend запущен (PID: $BACKEND_PID)"
cd ..

# Запускаем bot
echo "🤖 Запуск bot..."
cd bot
source venv/bin/activate
nohup python main.py > ../logs/bot.log 2>&1 &
BOT_PID=$!
echo "Bot запущен (PID: $BOT_PID)"
cd ..

# Проверяем, что nginx настроен правильно
echo "🌐 Проверка nginx конфигурации..."
nginx -t
if [ $? -eq 0 ]; then
    echo "Nginx конфигурация корректна"
    systemctl reload nginx
    echo "Nginx перезапущен для статических файлов"
else
    echo "❌ Ошибка в конфигурации nginx!"
    exit 1
fi

# Ждем запуска сервисов
sleep 5

echo ""
echo "✅ Все сервисы запущены!"
echo "📊 Статус:"
echo "  Backend:  https://projectmanager.chickenkiller.com/api"
echo "  Frontend: https://projectmanager.chickenkiller.com (nginx)"
echo "  Bot:      Готов к работе"
echo ""
echo "📋 Логи:"
echo "  Backend:  tail -f logs/backend.log"
echo "  Bot:      tail -f logs/bot.log"
echo "  Nginx:    tail -f /var/log/nginx/error.log"
echo ""
echo "🔄 Перезапуск: ./start_all.sh"
echo "🛑 Остановка: pkill -f 'python main.py'"
