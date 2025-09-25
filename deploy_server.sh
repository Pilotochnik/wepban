#!/bin/bash

echo "🚀 Установка Project Manager Bot на сервер..."

# Обновляем систему
echo "📦 Обновляем систему..."
apt update && apt upgrade -y

# Устанавливаем Node.js 18+
echo "📦 Устанавливаем Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Устанавливаем Python 3.11+
echo "📦 Устанавливаем Python..."
apt install python3.11 python3.11-venv python3-pip -y

# Устанавливаем PostgreSQL
echo "📦 Устанавливаем PostgreSQL..."
apt install postgresql postgresql-contrib -y

# Устанавливаем nginx
echo "📦 Устанавливаем nginx..."
apt install nginx -y

# Устанавливаем certbot для SSL
echo "📦 Устанавливаем certbot..."
apt install certbot python3-certbot-nginx -y

# Устанавливаем PM2 для управления процессами
echo "📦 Устанавливаем PM2..."
npm install -g pm2

# Создаем папку для проекта
echo "📁 Создаем папку проекта..."
mkdir -p /var/www/project-manager
cd /var/www/project-manager

# Создаем базу данных
echo "🗄️ Настраиваем базу данных..."
sudo -u postgres psql -c "CREATE DATABASE project_manager;"
sudo -u postgres psql -c "CREATE USER project_user WITH PASSWORD 'project_password123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE project_manager TO project_user;"

# Настраиваем nginx
echo "🌐 Настраиваем nginx..."
cat > /etc/nginx/sites-available/project-manager << 'EOF'
server {
    listen 80;
    server_name projectmanager.chickenkiller.com;

    # Frontend (порт 3000)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API (порт 8000)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name projectmanager.chickenkiller.com;

    # SSL сертификаты (будут добавлены certbot)
    ssl_certificate /etc/letsencrypt/live/projectmanager.chickenkiller.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/projectmanager.chickenkiller.com/privkey.pem;

    # Frontend (порт 3000)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API (порт 8000)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Активируем конфиг nginx
ln -s /etc/nginx/sites-available/project-manager /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "✅ Установка завершена!"
echo "📝 Теперь загрузите файлы проекта в /var/www/project-manager/"
echo "📝 Создайте .env файлы для backend и bot"
echo "📝 Запустите: ./start_all.sh"
