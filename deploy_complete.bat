@echo off
chcp 65001 >nul
echo Полный деплой проекта на сервер...

echo Шаг 1: Подключение к серверу...
ssh root@194.87.76.75 "cd /var/www/project-manager && chmod +x *.sh && ./setup_env.sh && ./start_all.sh && ./setup_ssl.sh"

echo Деплой завершен!
echo Проверьте работу сервисов:
echo - Frontend: https://projectmanager.chickenkiller.com
echo - Backend API: https://projectmanager.chickenkiller.com/api
echo - Telegram Bot: готов к работе
pause
