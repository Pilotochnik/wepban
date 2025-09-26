#!/bin/bash

echo "=== Исправление конфигурации сервера ==="

# 1. Останавливаем все процессы проекта
echo "Останавливаем процессы..."
pkill -f "python main.py"
pkill -f "vite preview"

# 2. Проверяем, что процессы остановлены
echo "Проверяем процессы..."
ps aux | grep -E "(python main.py|vite preview)" | grep -v grep

# 3. Устанавливаем правильную nginx конфигурацию
echo "Устанавливаем nginx конфигурацию..."
cat > /etc/nginx/sites-available/project-manager << 'EOF'
server {
    listen 80;
    server_name projectmanager.chickenkiller.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name projectmanager.chickenkiller.com;
    
    root /var/www/project-manager/frontend/dist;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/projectmanager.chickenkiller.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/projectmanager.chickenkiller.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 4. Активируем сайт
ln -sf /etc/nginx/sites-available/project-manager /etc/nginx/sites-enabled/

# 5. Проверяем конфигурацию nginx
echo "Проверяем nginx конфигурацию..."
nginx -t

# 6. Перезапускаем nginx
echo "Перезапускаем nginx..."
systemctl reload nginx

# 7. Запускаем бэкенд в фоне
echo "Запускаем бэкенд..."
cd /var/www/project-manager/backend
nohup python main.py > /var/www/project-manager/logs/backend.log 2>&1 &

# 8. Проверяем статус
echo "Проверяем статус..."
sleep 3
ps aux | grep -E "(python main.py|nginx)" | grep -v grep
netstat -tlnp | grep -E ":80|:443|:8000"

echo "=== Готово ==="
