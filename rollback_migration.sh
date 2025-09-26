#!/bin/bash

# 🔄 Скрипт отката миграции
# Возвращает проект на старый сервер в случае проблем

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

echo -e "${RED}🔄 ОТКАТ МИГРАЦИИ${NC}"
echo -e "${YELLOW}⚠️  ВНИМАНИЕ: Этот скрипт вернет проект на старый сервер!${NC}"
echo ""

# Подтверждение
read -p "Вы уверены, что хотите выполнить откат? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Откат отменен."
    exit 0
fi

echo -e "${BLUE}1. Остановка сервисов на новом сервере${NC}"
ssh root@${NEW_SERVER} "systemctl stop project-manager-backend project-manager-bot nginx" 2>/dev/null || true

echo -e "${BLUE}2. Запуск сервисов на старом сервере${NC}"
ssh root@${OLD_SERVER} "cd /var/www/project-manager && ./start_all.sh"

echo -e "${BLUE}3. Проверка работы старого сервера${NC}"
sleep 10

# Проверка доступности старого сервера
if curl -s https://${OLD_DOMAIN} >/dev/null; then
    echo -e "${GREEN}✅ Старый сервер работает${NC}"
else
    echo -e "${RED}❌ Проблемы со старым сервером${NC}"
fi

echo -e "${BLUE}4. Обновление DNS (если необходимо)${NC}"
echo -e "${YELLOW}⚠️  ВАЖНО: Верните DNS запись ${OLD_DOMAIN} на ${OLD_SERVER}${NC}"
echo -e "${YELLOW}   После обновления DNS подождите 5-10 минут${NC}"

echo -e "${BLUE}5. Финальная проверка${NC}"
echo "Проверяем доступность:"
echo "  - https://${OLD_DOMAIN}"
echo "  - https://${OLD_DOMAIN}/api/"
echo "  - https://${OLD_DOMAIN}/docs"

echo ""
echo -e "${GREEN}🎉 Откат завершен!${NC}"
echo -e "${YELLOW}📋 Следующие шаги:${NC}"
echo "1. Обновите DNS запись ${OLD_DOMAIN} -> ${OLD_SERVER}"
echo "2. Подождите 5-10 минут для распространения DNS"
echo "3. Проверьте работу: https://${OLD_DOMAIN}"
echo "4. Уведомите пользователей о восстановлении работы"
