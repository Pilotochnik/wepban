# 🚀 Развертывание на сервере

## Быстрый запуск

### 1. Подключитесь к серверу
```bash
ssh root@194.87.76.75
```

### 2. Загрузите файлы проекта
```bash
# С локального компьютера выполните:
./upload_to_server.bat
```

### 3. На сервере выполните установку
```bash
cd /var/www/project-manager
chmod +x *.sh
./deploy_server.sh
```

### 4. Настройте .env файлы
```bash
./setup_env.sh
# Отредактируйте backend/.env и bot/.env
nano backend/.env
nano bot/.env
```

### 5. Запустите все процессы
```bash
./start_all.sh
```

### 6. Настройте SSL
```bash
./setup_ssl.sh
```

## Управление процессами

```bash
# Статус процессов
pm2 status

# Логи
pm2 logs

# Перезапуск
pm2 restart all

# Остановка
pm2 stop all
```

## Доступ к приложению

- **Frontend**: https://projectmanager.chickenkiller.com
- **Backend API**: https://projectmanager.chickenkiller.com/api/
- **Telegram Bot**: Работает в фоне

## Настройка Telegram WebApp

В боте будет кнопка "🚀 Открыть веб-приложение" которая откроет веб-интерфейс прямо в Telegram!

## Структура файлов на сервере

```
/var/www/project-manager/
├── backend/          # FastAPI backend
├── bot/              # Telegram bot
├── frontend/         # React frontend
├── deploy_server.sh  # Скрипт установки
├── start_all.sh      # Скрипт запуска
├── setup_env.sh      # Скрипт настройки .env
└── setup_ssl.sh      # Скрипт настройки SSL
```
