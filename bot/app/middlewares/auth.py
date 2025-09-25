from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """Middleware для аутентификации пользователей"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Обработка middleware"""
        
        # Получаем пользователя из события
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        else:
            user = None
        
        if not user:
            logger.warning("Не удалось получить информацию о пользователе")
            return await handler(event, data)
        
        # Логируем активность пользователя
        logger.info(f"Пользователь {user.id} ({user.username or user.first_name}) отправил {type(event).__name__}")
        
        # Проверяем доступ к боту через API
        try:
            from app.services.api import APIService
            api_service = APIService()
            
            # Проверяем, есть ли пользователь в системе и активен ли он
            user_data = await api_service.check_user_access(user.id)
            
            if not user_data or not user_data.get('is_active', False):
                # Пользователь не найден или неактивен
                if hasattr(event, 'answer'):
                    await event.answer(
                        "❌ Доступ к боту ограничен.\n\n"
                        "Обратитесь к администратору для получения доступа к системе управления проектами."
                    )
                return  # Блокируем обработку
                
            # Сохраняем данные пользователя в контексте
            data['user_data'] = user_data
            
        except Exception as e:
            logger.error(f"Ошибка проверки доступа пользователя {user.id}: {e}")
            # В случае ошибки API разрешаем доступ (fallback)
            pass
        
        # Добавляем информацию о пользователе в данные
        data["user_id"] = user.id
        data["user_username"] = user.username
        data["user_first_name"] = user.first_name
        data["user_last_name"] = user.last_name
        
        return await handler(event, data)
