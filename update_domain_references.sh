#!/bin/bash

# 🔄 Скрипт обновления всех ссылок на домен в проекте
# Заменяет projectmanager.chickenkiller.com на webpan.chickenkiller.com

set -e

OLD_DOMAIN="projectmanager.chickenkiller.com"
NEW_DOMAIN="webpan.chickenkiller.com"

echo "🔄 Обновление ссылок на домен в проекте..."
echo "Старый домен: $OLD_DOMAIN"
echo "Новый домен: $NEW_DOMAIN"
echo ""

# Функция для замены в файле
replace_in_file() {
    local file="$1"
    if [ -f "$file" ]; then
        echo "Обновляем: $file"
        sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" "$file"
    fi
}

# Обновление конфигурационных файлов
echo "📁 Обновление конфигурационных файлов..."

# Backend конфигурация
replace_in_file "backend/app/core/config.py"

# Bot конфигурация
replace_in_file "bot/app/core/config.py"

# Frontend конфигурация
replace_in_file "frontend/vite.config.ts"

# Nginx конфигурации
replace_in_file "nginx-config.txt"
replace_in_file "nginx-config-fixed.txt"

# Скрипты развертывания
replace_in_file "deploy_server.sh"
replace_in_file "fix_server_ports.sh"
replace_in_file "setup_ssl.sh"

# Документация
replace_in_file "SERVER_DEPLOY.md"

# Скрипты проверки
replace_in_file "check_ports.py"

# HTML тестовые файлы
find . -name "*.html" -exec sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" {} \;

# Python тестовые файлы
find . -name "*.py" -exec sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" {} \;

# JavaScript/TypeScript файлы
find . -name "*.js" -o -name "*.ts" -o -name "*.tsx" | xargs sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" 2>/dev/null || true

# Batch файлы
find . -name "*.bat" -exec sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" {} \;

# Shell скрипты
find . -name "*.sh" -exec sed -i "s/$OLD_DOMAIN/$NEW_DOMAIN/g" {} \;

echo ""
echo "✅ Обновление завершено!"
echo "📋 Обновленные файлы:"
echo "   - backend/app/core/config.py"
echo "   - bot/app/core/config.py"
echo "   - frontend/vite.config.ts"
echo "   - nginx-config.txt"
echo "   - deploy_server.sh"
echo "   - и другие файлы проекта"
echo ""
echo "🚀 Теперь можно запускать migrate_to_new_server.sh"
