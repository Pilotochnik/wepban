@echo off
chcp 65001 >nul
echo Загрузка файлов на сервер...

REM Загружаем все файлы проекта на сервер
scp -r backend bot frontend *.sh *.bat *.md *.yml *.py root@194.87.76.75:/var/www/project-manager/

echo Файлы загружены на сервер!
echo Теперь подключитесь к серверу и выполните:
echo    ssh root@194.87.76.75
echo    cd /var/www/project-manager
echo    chmod +x *.sh
echo    ./setup_env.sh
echo    ./start_all.sh
echo    ./setup_ssl.sh
