#!/bin/bash

echo "🔒 Настройка SSL сертификата..."

# Получаем SSL сертификат
echo "📜 Получаем SSL сертификат..."
certbot --nginx -d projectmanager.chickenkiller.com --non-interactive --agree-tos --email admin@projectmanager.chickenkiller.com

# Настраиваем автообновление
echo "🔄 Настраиваем автообновление SSL..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ SSL сертификат настроен!"
echo "🌐 Теперь ваш сайт доступен по HTTPS: https://projectmanager.chickenkiller.com"
