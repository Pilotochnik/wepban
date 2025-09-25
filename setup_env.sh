#!/bin/bash

echo "⚙️ Настройка .env файлов..."

cd /var/www/project-manager

# Создаем .env для backend
echo "📝 Создаем .env для backend..."
cat > backend/.env << 'EOF'
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://projectmanager.chickenkiller.com
SECRET_KEY=your_secret_key_here_change_this
DB_HOST=localhost
DB_PORT=5432
DB_NAME=project_manager
DB_USER=project_user
DB_PASS=project_password123
OPENAI_API_KEY=your_openai_api_key_here
SENTRY_DSN=
ENVIRONMENT=production
EOF

# Создаем .env для bot
echo "📝 Создаем .env для bot..."
cat > bot/.env << 'EOF'
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://projectmanager.chickenkiller.com
BACKEND_URL=https://projectmanager.chickenkiller.com
OPENAI_API_KEY=your_openai_api_key_here
SENTRY_DSN=
ENVIRONMENT=production
EOF

echo "✅ .env файлы созданы!"
echo "📝 Отредактируйте их и укажите ваши токены:"
echo "  - BOT_TOKEN (токен Telegram бота)"
echo "  - OPENAI_API_KEY (ключ OpenAI)"
echo "  - SECRET_KEY (секретный ключ для JWT)"
echo ""
echo "📝 Файлы находятся в:"
echo "  - backend/.env"
echo "  - bot/.env"
