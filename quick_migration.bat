@echo off
REM 🚀 Быстрая миграция на новый европейский сервер
REM Windows batch файл для запуска миграции

echo.
echo ========================================
echo 🚀 МИГРАЦИЯ НА НОВЫЙ ЕВРОПЕЙСКИЙ СЕРВЕР
echo ========================================
echo.
echo Старый сервер: 194.87.76.75
echo Новый сервер: 88.218.122.213 (webpan.chickenkiller.com)
echo.

REM Проверка готовности
echo [1/4] Проверка готовности к миграции...
bash check_migration_readiness.sh
if %errorlevel% neq 0 (
    echo ❌ Проверка не пройдена. Исправьте ошибки и повторите.
    pause
    exit /b 1
)

echo.
echo [2/4] Обновление ссылок на домен в проекте...
bash update_domain_references.sh

echo.
echo [3/4] Запуск миграции...
echo ⚠️  ВНИМАНИЕ: Миграция займет 15-20 минут
echo ⚠️  Убедитесь, что DNS запись webpan.chickenkiller.com указывает на 88.218.122.213
echo.
pause

bash migrate_to_new_server.sh
if %errorlevel% neq 0 (
    echo ❌ Ошибка миграции. Проверьте логи.
    pause
    exit /b 1
)

echo.
echo [4/4] Переключение на новый сервер...
echo ⚠️  ВАЖНО: Обновите DNS запись webpan.chickenkiller.com -> 88.218.122.213
echo ⚠️  Подождите 5-10 минут для распространения DNS
echo.
pause

bash switch_to_new_server.sh

echo.
echo ========================================
echo ✅ МИГРАЦИЯ ЗАВЕРШЕНА!
echo ========================================
echo.
echo 🌐 Новый адрес: https://webpan.chickenkiller.com
echo 🤖 Telegram Bot: @wwwpan_bot
echo 📊 API: https://webpan.chickenkiller.com/api/
echo 📚 Docs: https://webpan.chickenkiller.com/docs
echo.
echo ✅ OpenAI теперь работает без проблем!
echo.
pause
