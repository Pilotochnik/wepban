#!/bin/bash

# 🔍 Скрипт проверки готовности к миграции
# Проверяет все компоненты перед переносом на новый сервер

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

OLD_SERVER="194.87.76.75"
NEW_SERVER="88.218.122.213"
OLD_DOMAIN="projectmanager.chickenkiller.com"
NEW_DOMAIN="webpan.chickenkiller.com"

echo -e "${BLUE}🔍 Проверка готовности к миграции${NC}"
echo ""

# Функция для проверки
check() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Проверяем $name... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        return 1
    fi
}

# Функция для проверки с выводом
check_with_output() {
    local name="$1"
    local command="$2"
    
    echo -e "${YELLOW}Проверяем $name:${NC}"
    eval "$command"
    echo ""
}

echo -e "${BLUE}1. Проверка текущего сервера ($OLD_SERVER)${NC}"

# Проверка доступности старого сервера
check "Доступность старого сервера" "ping -c 1 $OLD_SERVER"

# Проверка сервисов на старом сервере
check "Backend на старом сервере" "curl -s http://$OLD_SERVER:8000/docs | grep -q 'Swagger'"
check "Frontend на старом сервере" "curl -s https://$OLD_DOMAIN | grep -q 'html'"
check "Nginx на старом сервере" "curl -s -I https://$OLD_DOMAIN | grep -q '200 OK'"

# Проверка базы данных
check_with_output "База данных на старом сервере" "ssh root@$OLD_SERVER 'ls -la /var/www/project-manager/backend/project_manager.db'"

# Проверка логов
check_with_output "Логи на старом сервере" "ssh root@$OLD_SERVER 'ls -la /var/www/project-manager/logs/'"

echo -e "${BLUE}2. Проверка нового сервера ($NEW_SERVER)${NC}"

# Проверка доступности нового сервера
check "Доступность нового сервера" "ping -c 1 $NEW_SERVER"

# Проверка SSH доступности
check "SSH доступность нового сервера" "ssh -o ConnectTimeout=10 root@$NEW_SERVER 'echo test'"

# Проверка установленных пакетов на новом сервере
check_with_output "Установленные пакеты на новом сервере" "ssh root@$NEW_SERVER 'which nginx python3 nodejs npm certbot'"

echo -e "${BLUE}3. Проверка DNS${NC}"

# Проверка DNS записи
check_with_output "DNS запись для $NEW_DOMAIN" "nslookup $NEW_DOMAIN"

echo -e "${BLUE}4. Проверка файлов проекта${NC}"

# Проверка наличия ключевых файлов
check "Backend конфигурация" "[ -f 'backend/app/core/config.py' ]"
check "Bot конфигурация" "[ -f 'bot/app/core/config.py' ]"
check "Frontend конфигурация" "[ -f 'frontend/vite.config.ts' ]"
check "Nginx конфигурация" "[ -f 'nginx-config.txt' ]"
check "Скрипт миграции" "[ -f 'migrate_to_new_server.sh' ]"

# Проверка .env файлов на старом сервере
check_with_output ".env файлы на старом сервере" "ssh root@$OLD_SERVER 'ls -la /var/www/project-manager/backend/.env /var/www/project-manager/bot/.env'"

echo -e "${BLUE}5. Проверка зависимостей${NC}"

# Проверка requirements.txt
check "Backend requirements.txt" "[ -f 'backend/requirements.txt' ]"
check "Bot requirements.txt" "[ -f 'bot/requirements.txt' ]"
check "Frontend package.json" "[ -f 'frontend/package.json' ]"

echo -e "${BLUE}6. Проверка SSL сертификатов${NC}"

# Проверка SSL на старом сервере
check_with_output "SSL сертификат на старом сервере" "curl -s -I https://$OLD_DOMAIN | grep -i 'server\\|ssl'"

echo -e "${BLUE}7. Проверка Telegram Bot${NC}"

# Проверка логов бота
check_with_output "Логи бота" "ssh root@$OLD_SERVER 'tail -5 /var/www/project-manager/logs/bot.log'"

echo -e "${BLUE}8. Проверка OpenAI API${NC}"

# Проверка OpenAI API ключа
check_with_output "OpenAI API ключ" "ssh root@$OLD_SERVER 'grep -q OPENAI_API_KEY /var/www/project-manager/backend/.env'"

echo ""
echo -e "${GREEN}🎉 Проверка завершена!${NC}"
echo ""
echo -e "${YELLOW}📋 Рекомендации перед миграцией:${NC}"
echo "1. Убедитесь, что DNS запись $NEW_DOMAIN указывает на $NEW_SERVER"
echo "2. Создайте полный бэкап базы данных"
echo "3. Уведомите пользователей о плановом обслуживании"
echo "4. Подготовьте план отката на случай проблем"
echo ""
echo -e "${GREEN}🚀 Готово к миграции! Запустите: ./migrate_to_new_server.sh${NC}"
