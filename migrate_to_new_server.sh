#!/bin/bash

# 🚀 Скрипт миграции на новый европейский сервер
# Старый сервер: 194.87.76.75
# Новый сервер: 88.218.122.213 (webpan.chickenkiller.com)

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфигурация
OLD_SERVER="194.87.76.75"
NEW_SERVER="88.218.122.213"
OLD_DOMAIN="projectmanager.chickenkiller.com"
NEW_DOMAIN="webpan.chickenkiller.com"
PROJECT_DIR="/var/www/project-manager"

echo -e "${BLUE}🚀 Начинаем миграцию на новый европейский сервер${NC}"
echo -e "${YELLOW}Старый сервер: ${OLD_SERVER}${NC}"
echo -e "${YELLOW}Новый сервер: ${NEW_SERVER} (${NEW_DOMAIN})${NC}"
echo ""

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Шаг 1: Создание бэкапа с текущего сервера
log "Шаг 1: Создание полного бэкапа с текущего сервера"
ssh root@${OLD_SERVER} "cd ${PROJECT_DIR} && tar -czf /tmp/project-manager-backup-$(date +%Y%m%d_%H%M%S).tar.gz ."
if [ $? -eq 0 ]; then
    log "✅ Бэкап создан успешно"
else
    error "❌ Ошибка создания бэкапа"
fi

# Шаг 2: Подготовка нового сервера
log "Шаг 2: Подготовка нового сервера"
ssh root@${NEW_SERVER} << 'EOF'
# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y nginx certbot python3-certbot-nginx python3 python3-pip python3-venv nodejs npm git curl wget unzip

# Создание директории проекта
mkdir -p /var/www/project-manager
chown -R www-data:www-data /var/www/project-manager

# Создание директории для логов
mkdir -p /var/www/project-manager/logs
chown -R www-data:www-data /var/www/project-manager/logs

echo "✅ Новый сервер подготовлен"
EOF

# Шаг 3: Копирование файлов проекта
log "Шаг 3: Копирование файлов проекта"
scp -r root@${OLD_SERVER}:${PROJECT_DIR}/* root@${NEW_SERVER}:${PROJECT_DIR}/

# Шаг 4: Обновление конфигурационных файлов
log "Шаг 4: Обновление конфигурационных файлов на новом сервере"

# Обновление backend конфигурации
ssh root@${NEW_SERVER} "sed -i 's/${OLD_DOMAIN}/${NEW_DOMAIN}/g' ${PROJECT_DIR}/backend/app/core/config.py"

# Обновление bot конфигурации
ssh root@${NEW_SERVER} "sed -i 's/${OLD_DOMAIN}/${NEW_DOMAIN}/g' ${PROJECT_DIR}/bot/app/core/config.py"

# Обновление frontend конфигурации
ssh root@${NEW_SERVER} "sed -i 's/${OLD_DOMAIN}/${NEW_DOMAIN}/g' ${PROJECT_DIR}/frontend/vite.config.ts"

# Шаг 5: Настройка Nginx
log "Шаг 5: Настройка Nginx на новом сервере"
ssh root@${NEW_SERVER} << EOF
# Создание конфигурации Nginx
cat > /etc/nginx/sites-available/${NEW_DOMAIN} << 'NGINX_EOF'
server {
    listen 80;
    server_name ${NEW_DOMAIN};
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${NEW_DOMAIN};
    
    root ${PROJECT_DIR}/frontend/dist;
    index index.html;

    # SSL сертификаты (будут добавлены certbot)
    ssl_certificate /etc/letsencrypt/live/${NEW_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${NEW_DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Frontend (статические файлы)
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # API docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX_EOF

# Активация сайта
ln -sf /etc/nginx/sites-available/${NEW_DOMAIN} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации
nginx -t
echo "✅ Nginx настроен"
EOF

# Шаг 6: Установка SSL сертификата
log "Шаг 6: Установка SSL сертификата"
ssh root@${NEW_SERVER} << EOF
# Временная конфигурация для получения сертификата
cat > /etc/nginx/sites-available/${NEW_DOMAIN}-temp << 'TEMP_EOF'
server {
    listen 80;
    server_name ${NEW_DOMAIN};
    
    root ${PROJECT_DIR}/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
TEMP_EOF

# Активация временной конфигурации
ln -sf /etc/nginx/sites-available/${NEW_DOMAIN}-temp /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/${NEW_DOMAIN}
nginx -t && systemctl reload nginx

# Получение SSL сертификата
certbot --nginx -d ${NEW_DOMAIN} --non-interactive --agree-tos --email admin@${NEW_DOMAIN}

# Активация финальной конфигурации
rm -f /etc/nginx/sites-enabled/${NEW_DOMAIN}-temp
ln -sf /etc/nginx/sites-available/${NEW_DOMAIN} /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo "✅ SSL сертификат установлен"
EOF

# Шаг 7: Установка зависимостей и настройка окружения
log "Шаг 7: Установка зависимостей на новом сервере"
ssh root@${NEW_SERVER} << EOF
cd ${PROJECT_DIR}

# Установка зависимостей backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend зависимости установлены"

# Установка зависимостей bot
cd ../bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Bot зависимости установлены"

# Установка зависимостей frontend
cd ../frontend
npm install
npm run build
echo "✅ Frontend зависимости установлены и собран"
EOF

# Шаг 8: Настройка .env файлов
log "Шаг 8: Настройка .env файлов"
ssh root@${NEW_SERVER} << EOF
cd ${PROJECT_DIR}

# Копирование .env файлов с старого сервера
scp root@${OLD_SERVER}:${PROJECT_DIR}/backend/.env backend/
scp root@${OLD_SERVER}:${PROJECT_DIR}/bot/.env bot/

# Обновление URL в .env файлах
sed -i 's/${OLD_DOMAIN}/${NEW_DOMAIN}/g' backend/.env
sed -i 's/${OLD_DOMAIN}/${NEW_DOMAIN}/g' bot/.env

echo "✅ .env файлы настроены"
EOF

# Шаг 9: Запуск сервисов
log "Шаг 9: Запуск сервисов на новом сервере"
ssh root@${NEW_SERVER} << EOF
cd ${PROJECT_DIR}

# Создание systemd сервисов
cat > /etc/systemd/system/project-manager-backend.service << 'SERVICE_EOF'
[Unit]
Description=Project Manager Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=${PROJECT_DIR}/backend
Environment=PATH=${PROJECT_DIR}/backend/venv/bin
ExecStart=${PROJECT_DIR}/backend/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_EOF

cat > /etc/systemd/system/project-manager-bot.service << 'SERVICE_EOF'
[Unit]
Description=Project Manager Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=${PROJECT_DIR}/bot
Environment=PATH=${PROJECT_DIR}/bot/venv/bin
ExecStart=${PROJECT_DIR}/bot/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Активация и запуск сервисов
systemctl daemon-reload
systemctl enable project-manager-backend
systemctl enable project-manager-bot
systemctl start project-manager-backend
systemctl start project-manager-bot

# Проверка статуса
sleep 5
systemctl status project-manager-backend --no-pager
systemctl status project-manager-bot --no-pager

echo "✅ Сервисы запущены"
EOF

# Шаг 10: Финальная проверка
log "Шаг 10: Финальная проверка"
ssh root@${NEW_SERVER} << EOF
# Проверка портов
netstat -tlnp | grep -E ':(80|443|8000)'

# Проверка сервисов
systemctl is-active project-manager-backend
systemctl is-active project-manager-bot

# Проверка Nginx
systemctl is-active nginx

# Проверка SSL
curl -I https://${NEW_DOMAIN} 2>/dev/null | head -1

echo "✅ Проверка завершена"
EOF

# Шаг 11: Обновление DNS (информация для пользователя)
log "Шаг 11: Обновление DNS"
echo -e "${YELLOW}⚠️  ВАЖНО: Обновите DNS запись для ${NEW_DOMAIN}${NC}"
echo -e "${YELLOW}   Установите A-запись: ${NEW_DOMAIN} -> ${NEW_SERVER}${NC}"
echo -e "${YELLOW}   После обновления DNS подождите 5-10 минут для распространения${NC}"

# Шаг 12: Создание скрипта для переключения
log "Шаг 12: Создание скрипта переключения"
cat > switch_to_new_server.sh << 'SWITCH_EOF'
#!/bin/bash

# Скрипт для переключения на новый сервер
# Выполните после обновления DNS

echo "🔄 Переключение на новый сервер..."

# Остановка старых сервисов
ssh root@194.87.76.75 "systemctl stop project-manager-backend project-manager-bot 2>/dev/null || true"

# Проверка нового сервера
curl -I https://webpan.chickenkiller.com 2>/dev/null | head -1

if [ $? -eq 0 ]; then
    echo "✅ Новый сервер работает!"
    echo "🌐 Приложение доступно по адресу: https://webpan.chickenkiller.com"
else
    echo "❌ Новый сервер недоступен. Проверьте DNS и настройки."
fi
SWITCH_EOF

chmod +x switch_to_new_server.sh

echo ""
echo -e "${GREEN}🎉 Миграция завершена!${NC}"
echo -e "${BLUE}📋 Следующие шаги:${NC}"
echo -e "1. ${YELLOW}Обновите DNS запись: ${NEW_DOMAIN} -> ${NEW_SERVER}${NC}"
echo -e "2. ${YELLOW}Подождите 5-10 минут для распространения DNS${NC}"
echo -e "3. ${YELLOW}Выполните: ./switch_to_new_server.sh${NC}"
echo -e "4. ${YELLOW}Проверьте работу: https://${NEW_DOMAIN}${NC}"
echo ""
echo -e "${GREEN}✅ OpenAI будет работать без проблем на европейском сервере!${NC}"
