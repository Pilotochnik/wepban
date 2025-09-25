from aiogram import Router
from .start import router as start_router
from .webapp import router as webapp_router
from .voice import router as voice_router
from .photo import router as photo_router
from .text import router as text_router
from .callbacks import router as callbacks_router
from .admin import router as admin_router

router = Router()

router.include_router(start_router)  # Команды должны быть первыми
router.include_router(admin_router)  # Админ-панель
router.include_router(webapp_router)
router.include_router(callbacks_router)  # Callback кнопки
router.include_router(voice_router)  # Голосовые сообщения
router.include_router(photo_router)  # Фото
router.include_router(text_router)   # Текстовые сообщения в конце
