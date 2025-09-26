# 🚀 Руководство по миграции на новый европейский сервер

## 📋 Обзор

Этот набор скриптов обеспечивает быстрый и бесшовный перенос проекта с текущего сервера на новый европейский сервер, где OpenAI API будет работать без проблем.

### Серверы
- **Старый сервер**: 194.87.76.75 (projectmanager.chickenkiller.com)
- **Новый сервер**: 88.218.122.213 (webpan.chickenkiller.com)

## 🔧 Подготовка

### 1. Обновление ссылок в проекте
```bash
chmod +x update_domain_references.sh
./update_domain_references.sh
```

### 2. Проверка готовности
```bash
chmod +x check_migration_readiness.sh
./check_migration_readiness.sh
```

## 🚀 Миграция

### Основной скрипт миграции
```bash
chmod +x migrate_to_new_server.sh
./migrate_to_new_server.sh
```

### Что делает скрипт миграции:

1. **Создание бэкапа** с текущего сервера
2. **Подготовка нового сервера** (установка пакетов, настройка окружения)
3. **Копирование файлов** проекта
4. **Обновление конфигураций** (домены, URL)
5. **Настройка Nginx** с правильной конфигурацией
6. **Установка SSL сертификата** через Let's Encrypt
7. **Установка зависимостей** (Python, Node.js)
8. **Настройка .env файлов**
9. **Создание systemd сервисов**
10. **Запуск всех сервисов**
11. **Финальная проверка**

## 🔄 Переключение

После обновления DNS выполните:
```bash
chmod +x switch_to_new_server.sh
./switch_to_new_server.sh
```

## 🔙 Откат (если что-то пошло не так)

```bash
chmod +x rollback_migration.sh
./rollback_migration.sh
```

## 📊 Проверка после миграции

### 1. Проверка доступности
- https://webpan.chickenkiller.com
- https://webpan.chickenkiller.com/api/
- https://webpan.chickenkiller.com/docs

### 2. Проверка Telegram Bot
- Отправьте `/start` боту
- Проверьте создание задач через AI

### 3. Проверка AI функциональности
- Отправьте сообщение боту: "Создай задачу: купить молоко"
- AI должен работать без ошибок региона

## 🛠️ Ручные шаги

### Обновление DNS
1. Войдите в панель управления DNS
2. Измените A-запись: `webpan.chickenkiller.com` -> `88.218.122.213`
3. Подождите 5-10 минут для распространения

### Проверка сертификатов
```bash
# На новом сервере
certbot certificates
nginx -t
systemctl status nginx
```

### Проверка сервисов
```bash
# На новом сервере
systemctl status project-manager-backend
systemctl status project-manager-bot
journalctl -u project-manager-backend -f
journalctl -u project-manager-bot -f
```

## 🔍 Диагностика проблем

### Проблемы с SSL
```bash
# Проверка сертификата
openssl s_client -connect webpan.chickenkiller.com:443 -servername webpan.chickenkiller.com

# Переустановка сертификата
certbot --nginx -d webpan.chickenkiller.com --force-renewal
```

### Проблемы с сервисами
```bash
# Перезапуск сервисов
systemctl restart project-manager-backend
systemctl restart project-manager-bot
systemctl restart nginx

# Проверка логов
tail -f /var/www/project-manager/logs/backend.log
tail -f /var/www/project-manager/logs/bot.log
```

### Проблемы с базой данных
```bash
# Проверка файла БД
ls -la /var/www/project-manager/backend/project_manager.db

# Восстановление из бэкапа
cp /var/www/project-manager/backups/project_manager_backup_latest.db /var/www/project-manager/backend/project_manager.db
```

## 📁 Структура файлов миграции

```
├── migrate_to_new_server.sh      # Основной скрипт миграции
├── update_domain_references.sh   # Обновление ссылок на домен
├── check_migration_readiness.sh  # Проверка готовности
├── rollback_migration.sh         # Скрипт отката
├── switch_to_new_server.sh       # Переключение на новый сервер
└── MIGRATION_GUIDE.md           # Это руководство
```

## ⚡ Преимущества нового сервера

1. **OpenAI API работает** без блокировок региона
2. **Лучшая производительность** (европейский дата-центр)
3. **Стабильное соединение** с AI сервисами
4. **Современная инфраструктура**

## 🆘 Поддержка

В случае проблем:
1. Проверьте логи сервисов
2. Выполните диагностику
3. При необходимости используйте скрипт отката
4. Обратитесь к администратору

---

**Время миграции**: ~15-20 минут  
**Время простоя**: ~2-3 минуты (только при переключении DNS)  
**Сложность**: Автоматизированная (требует только обновления DNS)
