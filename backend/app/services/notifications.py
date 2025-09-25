import httpx
import json
from typing import Optional, Dict, Any
from app.core.config import settings
from app.models.user import User
from app.models.approval import ApprovalRequest, ActionType
import logging

logger = logging.getLogger(__name__)

class TelegramNotificationService:
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML"
                }
                
                if reply_markup:
                    payload["reply_markup"] = json.dumps(reply_markup)
                
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json=payload
                )
                
                if response.status_code == 200:
                    logger.info(f"Уведомление отправлено в чат {chat_id}")
                    return True
                else:
                    logger.error(f"Ошибка отправки уведомления: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")
            return False
    
    async def notify_approval_request(self, creator: User, approval: ApprovalRequest) -> bool:
        """Уведомление создателя о новом запросе на одобрение"""
        action_labels = {
            ActionType.CREATE_TASK: "создание задачи",
            ActionType.UPDATE_TASK: "изменение задачи", 
            ActionType.DELETE_TASK: "удаление задачи",
            ActionType.CREATE_PROJECT: "создание проекта",
            ActionType.UPDATE_PROJECT: "изменение проекта",
            ActionType.DELETE_PROJECT: "удаление проекта",
            ActionType.ADD_USER_TO_PROJECT: "добавление пользователя в проект",
            ActionType.REMOVE_USER_FROM_PROJECT: "удаление пользователя из проекта"
        }
        
        action_text = action_labels.get(approval.action_type, str(approval.action_type))
        
        message = f"""🔔 <b>Новый запрос на одобрение</b>

👤 <b>От:</b> {approval.requester.first_name} {approval.requester.last_name}
📋 <b>Действие:</b> {action_text}
📅 <b>Время:</b> {approval.created_at.strftime('%d.%m.%Y %H:%M')}

💬 <b>Детали:</b>
{self._format_action_data(approval.action_data)}

Для просмотра и одобрения перейдите в админ панель."""
        
        # Создаем inline клавиатуру для быстрого одобрения
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ Одобрить",
                        "callback_data": f"approve:{approval.id}"
                    },
                    {
                        "text": "❌ Отклонить", 
                        "callback_data": f"reject:{approval.id}"
                    }
                ],
                [
                    {
                        "text": "📋 Открыть админ панель",
                        "web_app": {"url": f"{settings.WEBAPP_URL}/admin"}
                    }
                ]
            ]
        }
        
        return await self.send_message(creator.telegram_id, message, reply_markup)
    
    async def notify_approval_result(self, requester: User, approval: ApprovalRequest) -> bool:
        """Уведомление пользователя о результате одобрения"""
        status_emoji = "✅" if approval.status.value == "approved" else "❌"
        status_text = "одобрено" if approval.status.value == "approved" else "отклонено"
        
        action_labels = {
            ActionType.CREATE_TASK: "создание задачи",
            ActionType.UPDATE_TASK: "изменение задачи",
            ActionType.DELETE_TASK: "удаление задачи", 
            ActionType.CREATE_PROJECT: "создание проекта",
            ActionType.UPDATE_PROJECT: "изменение проекта",
            ActionType.DELETE_PROJECT: "удаление проекта",
            ActionType.ADD_USER_TO_PROJECT: "добавление пользователя в проект",
            ActionType.REMOVE_USER_FROM_PROJECT: "удаление пользователя из проекта"
        }
        
        action_text = action_labels.get(approval.action_type, str(approval.action_type))
        
        message = f"""{status_emoji} <b>Запрос на одобрение {status_text}</b>

📋 <b>Действие:</b> {action_text}
👤 <b>Рассмотрел:</b> {approval.approver.first_name} {approval.approver.last_name}
📅 <b>Время:</b> {approval.reviewed_at.strftime('%d.%m.%Y %H:%M') if approval.reviewed_at else 'Не указано'}"""
        
        if approval.review_comment:
            message += f"\n\n💬 <b>Комментарий:</b>\n{approval.review_comment}"
        
        return await self.send_message(requester.telegram_id, message)
    
    async def notify_user_added(self, user: User, added_by: User) -> bool:
        """Уведомление о добавлении пользователя в систему"""
        message = f"""🎉 <b>Добро пожаловать в систему управления проектами!</b>

👤 <b>Вас добавил:</b> {added_by.first_name} {added_by.last_name}
🔑 <b>Ваша роль:</b> {self._get_role_label(user.role)}
📱 <b>Telegram ID:</b> {user.telegram_id}

Теперь вы можете использовать бота для работы с проектами!"""
        
        return await self.send_message(user.telegram_id, message)
    
    async def notify_user_status_changed(self, user: User, is_active: bool) -> bool:
        """Уведомление об изменении статуса пользователя"""
        status_text = "активирован" if is_active else "заблокирован"
        status_emoji = "✅" if is_active else "❌"
        
        message = f"""{status_emoji} <b>Статус аккаунта изменен</b>

Ваш аккаунт был {status_text}.

{f"Теперь вы можете использовать все функции системы!" if is_active else "Обратитесь к администратору для получения доступа."}"""
        
        return await self.send_message(user.telegram_id, message)
    
    def _format_action_data(self, action_data: Optional[str]) -> str:
        """Форматирование данных действия для отображения"""
        if not action_data:
            return "Нет дополнительных данных"
        
        try:
            data = json.loads(action_data)
            if isinstance(data, dict):
                lines = []
                for key, value in data.items():
                    if key == "title":
                        lines.append(f"📝 <b>Название:</b> {value}")
                    elif key == "description":
                        lines.append(f"📄 <b>Описание:</b> {value[:100]}{'...' if len(str(value)) > 100 else ''}")
                    elif key == "priority":
                        lines.append(f"⚡ <b>Приоритет:</b> {value}")
                    elif key == "deadline":
                        lines.append(f"⏰ <b>Дедлайн:</b> {value}")
                    elif key == "project_name":
                        lines.append(f"📂 <b>Проект:</b> {value}")
                    else:
                        lines.append(f"<b>{key}:</b> {value}")
                return "\n".join(lines)
            else:
                return str(data)
        except:
            return action_data
    
    def _get_role_label(self, role: str) -> str:
        """Получение читаемого названия роли"""
        labels = {
            "creator": "Создатель",
            "foreman": "Прораб", 
            "worker": "Рабочий",
            "viewer": "Наблюдатель"
        }
        return labels.get(role, role)

# Глобальный экземпляр сервиса
notification_service = TelegramNotificationService()
