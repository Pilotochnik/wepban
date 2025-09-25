import httpx
import asyncio
from typing import Dict, List, Any
from app.core.config import settings


class APIService:
    def __init__(self):
        self.base_url = settings.BACKEND_URL
        self.WEBAPP_URL = settings.WEBAPP_URL
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Базовый метод для HTTP запросов"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/api/v1{endpoint}"
            
            try:
                if method.upper() == "GET":
                    response = await client.get(url, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url)
                else:
                    raise ValueError(f"Неподдерживаемый HTTP метод: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPError as e:
                print(f"HTTP Error: {e}")
                print(f"URL: {url}")
                print(f"Data: {data}")
                raise Exception(f"Ошибка API запроса: {str(e)}")
            except Exception as e:
                print(f"General Error: {e}")
                raise Exception(f"Ошибка API запроса: {str(e)}")
    
    async def register_user(self, user_data: Dict) -> Dict:
        """Регистрация пользователя"""
        return await self._make_request("POST", "/users/register", user_data)
    
    async def authenticate_user(self, telegram_id: int) -> Dict:
        """Аутентификация пользователя"""
        return await self._make_request("POST", "/users/auth", {"telegram_id": telegram_id})
    
    async def get_user_projects(self, telegram_id: int) -> List[Dict]:
        """Получение проектов пользователя"""
        # Сначала получаем токен
        auth_data = await self.authenticate_user(telegram_id)
        token = auth_data["access_token"]
        
        # Затем делаем запрос с токеном
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/api/v1/projects/", headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def create_task(self, task_data: Dict, telegram_id: int) -> Dict:
        """Создание задачи"""
        print(f"Creating task with data: {task_data}")
        
        # Получаем токен
        auth_data = await self.authenticate_user(telegram_id)
        token = auth_data["access_token"]
        
        # Создаем задачу
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            print(f"Sending POST to: {self.base_url}/api/v1/tasks/")
            print(f"Headers: {headers}")
            print(f"Data: {task_data}")
            
            response = await client.post(
                f"{self.base_url}/api/v1/tasks/",
                headers=headers,
                json=task_data
            )
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
    
    async def save_photo_for_task(self, telegram_id: int, photo_path: str, task_id: int) -> bool:
        """Сохранение фото для задачи"""
        try:
            # Получаем токен
            auth_data = await self.authenticate_user(telegram_id)
            token = auth_data["access_token"]
            
            # Открываем файл и отправляем
            with open(photo_path, 'rb') as photo_file:
                files = {'photo': photo_file}
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    headers = {"Authorization": f"Bearer {token}"}
                    response = await client.post(
                        f"{self.base_url}/api/v1/photos/tasks/{task_id}/photo/",
                        headers=headers,
                        files=files
                    )
                    
                    print(f"Photo upload response: {response.status_code}")
                    print(f"Photo upload response text: {response.text}")
                    return response.status_code == 200
                    
        except Exception as e:
                    print(f"Error saving photo: {e}")
                    return False

    async def review_approval(self, approval_id: int, status: str) -> bool:
        """Одобрение или отклонение запроса"""
        try:
            # Получаем токен для создателя
            auth_data = await self.authenticate_user(434532312)  # ID создателя
            token = auth_data["access_token"]
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.post(
                    f"{self.base_url}/api/v1/admin/approvals/{approval_id}/review",
                    headers=headers,
                    json={"status": status}
                )
                
                print(f"Review approval response: {response.status_code}")
                return response.status_code == 200
                
        except Exception as e:
            print(f"Error reviewing approval: {e}")
            return False

    async def check_user_access(self, telegram_id: int) -> dict:
        """Проверка доступа пользователя к боту"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/users/check-access/{telegram_id}"
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"is_active": False}
                    
        except Exception as e:
            print(f"Error checking user access: {e}")
            return {"is_active": False}
    
    async def create_task_from_ai_data(self, telegram_id: int, task_data: Dict) -> Dict:
        """Создание задачи из данных AI"""
        # Получаем токен
        auth_data = await self.authenticate_user(telegram_id)
        token = auth_data["access_token"]
        
        # Создаем задачу
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"{self.base_url}/api/v1/ai/create-task-from-text/",
                headers=headers,
                json={"text": task_data.get("original_text", "")}
            )
            response.raise_for_status()
            return response.json()
    
    async def send_notification(self, telegram_id: int, message: str) -> bool:
        """Отправка уведомления пользователю"""
        # Здесь должна быть интеграция с Telegram Bot API для отправки уведомлений
        # В реальном приложении это будет отдельный сервис уведомлений
        try:
            # Логика отправки уведомления
            return True
        except Exception:
            return False
