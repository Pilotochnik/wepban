# 🚀 Руководство по настройке Project Manager Bot

## 📋 Требования

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Telegram Bot Token
- OpenAI API Key

## 🔧 Пошаговая настройка

### 1. Создание .env файла

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# Telegram Bot - ЗАМЕНИТЕ НА ВАШИ РЕАЛЬНЫЕ ДАННЫЕ
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
WEBAPP_URL=http://localhost:3000

# Database - PostgreSQL настройки
DB_HOST=localhost
DB_PORT=5432
DB_NAME=project_manager
DB_USER=postgres
DB_PASS=password

# Security - СГЕНЕРИРУЙТЕ СВОЙ СЕКРЕТНЫЙ КЛЮЧ
SECRET_KEY=your_super_secret_key_here_make_it_very_long_and_random_at_least_32_characters

# OpenAI API - ПОЛУЧИТЕ НА https://platform.openai.com/
OPENAI_API_KEY=sk-your-openai-api-key-here

# Monitoring - Необязательно
SENTRY_DSN=

# Environment
ENVIRONMENT=development
```

### 2. Получение Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Введите имя для вашего бота (например: "My Project Manager Bot")
4. Введите username для бота (например: "my_project_manager_bot")
5. Скопируйте полученный токен и вставьте в `BOT_TOKEN`

### 3. Получение OpenAI API Key

1. Зарегистрируйтесь на [OpenAI Platform](https://platform.openai.com/)
2. Перейдите в раздел [API Keys](https://platform.openai.com/api-keys)
3. Нажмите "Create new secret key"
4. Скопируйте ключ и вставьте в `OPENAI_API_KEY`

### 4. Настройка PostgreSQL

#### Windows (через установщик):
1. Скачайте PostgreSQL с [официального сайта](https://www.postgresql.org/download/windows/)
2. Установите с настройками по умолчанию
3. Запомните пароль для пользователя `postgres`

#### Или через Docker:
```bash
docker run --name postgres-pm -e POSTGRES_PASSWORD=password -e POSTGRES_DB=project_manager -p 5432:5432 -d postgres:15
```

### 5. Установка зависимостей

Зависимости уже установлены! Если нужно переустановить:

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 6. Настройка базы данных

```bash
# Перейдите в папку backend
cd backend

# Выполните миграции
alembic upgrade head
```

### 7. Запуск приложения

#### Терминал 1 - Backend:
```bash
cd backend
python main.py
```

#### Терминал 2 - Frontend:
```bash
cd frontend
npm run dev
```

#### Терминал 3 - Telegram Bot:
```bash
cd bot
python main.py
```

## 🌐 Доступ к приложению

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Тестирование

### 1. Создание тестового пользователя

Откройте http://localhost:8000/docs и используйте endpoint:
```
POST /api/v1/users/register
```

Тело запроса:
```json
{
  "telegram_id": 123456789,
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User"
}
```

### 2. Тестирование бота

1. Найдите вашего бота в Telegram по username
2. Отправьте команду `/start`
3. Отправьте голосовое сообщение: "Создай задачу: купить корм для офиса до завтра"

## 🔧 Устранение неполадок

### Ошибка подключения к БД:
- Проверьте, что PostgreSQL запущен
- Проверьте настройки в .env файле
- Убедитесь, что база данных `project_manager` создана

### Ошибка OpenAI API:
- Проверьте, что API ключ корректный
- Убедитесь, что у вас есть доступ к GPT-4o-mini
- Проверьте баланс аккаунта OpenAI

### Ошибка Telegram Bot:
- Проверьте токен бота
- Убедитесь, что бот не заблокирован
- Проверьте, что webhook не настроен (для polling режима)

## 📝 Полезные команды

```bash
# Создание новой миграции
cd backend
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграций
alembic downgrade -1

# Перезапуск frontend
cd frontend
npm run dev

# Проверка статуса PostgreSQL
pg_isready -h localhost -p 5432
```
