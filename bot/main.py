import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.handlers import router
from app.middlewares import AuthMiddleware
from app.core.config import settings

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    # Создаем бота и диспетчер
    bot = Bot(
        token=settings.BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )
    dp = Dispatcher()
    
    # Регистрируем middleware
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    
    # Регистрируем роутеры
    dp.include_router(router)
    
    # Запускаем бота
    logger.info("Запуск Telegram Bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
