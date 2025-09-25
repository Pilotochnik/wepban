import openai
from typing import Dict, List, Any
import tempfile
import os
from app.core.config import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


class AIAssistant:
    def __init__(self):
        self.client = client
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Преобразование голосового сообщения в текст"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Ошибка распознавания речи: {str(e)}")
    
    async def analyze_text_request(self, text: str, user_projects: List[Dict]) -> Dict[str, Any]:
        """Анализ текстового запроса для создания задачи"""
        projects_info = "\n".join([f"- {p['name']} (ID: {p['id']})" for p in user_projects])
        
        # Логика умного распределения по проектам
        project_keywords = {
            "дом": ["дом", "убрать", "помыть", "почистить", "приготовить", "посуда", "полы", "комната"],
            "работа": ["работа", "клиент", "проект", "встреча", "презентация", "отчет", "звонок", "офис"],
            "личное": ["врач", "курсы", "спорт", "магазин", "покупка", "личное", "здоровье", "учеба"]
        }
        
        # Определяем подходящий проект
        assigned_project_id = None
        text_lower = text.lower()
        
        for category, keywords in project_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                # Ищем проект с похожим названием
                for project in user_projects:
                    if category in project["name"].lower():
                        assigned_project_id = project["id"]
                        break
                break
        
        # Если проект не найден, берем первый доступный
        if not assigned_project_id and user_projects:
            assigned_project_id = user_projects[0]["id"]
        
        prompt = f"""
Создай задачу из текста и определи приоритет.

Текст: "{text}"

Доступные проекты:
{projects_info}

Выбранный проект ID: {assigned_project_id}

Отвечай в JSON формате:
{{
    "title": "Название задачи",
    "description": "Подробное описание задачи", 
    "project_id": {assigned_project_id},
    "priority": "low|medium|high|urgent",
    "deadline": null
}}

Правила приоритета:
- "срочно", "быстро", "сегодня" → "urgent"
- "важно", "приоритет" → "high" 
- "не важно", "потом" → "low"
- остальное → "medium"

Примеры:
- "срочно помыть посуду" → {{"title": "Помыть посуду", "description": "Срочно помыть посуду", "project_id": {assigned_project_id}, "priority": "urgent", "deadline": null}}
- "купить молоко в магазине" → {{"title": "Купить молоко", "description": "Купить молоко в магазине", "project_id": {assigned_project_id}, "priority": "medium", "deadline": null}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты AI ассистент для создания задач. Отвечай только в JSON формате."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            import json
            content = response.choices[0].message.content.strip()
            print(f"AI Response: {content}")
            
            # Проверяем, что ответ не пустой
            if not content:
                raise Exception("AI вернул пустой ответ")
            
            # Очищаем ответ от markdown блоков
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            print(f"Cleaned AI Response: {content}")
            result = json.loads(content)
            
            # Проверяем, является ли запрос задачей
            if result.get("status") == "not_task":
                return {"status": "not_task", "message": "Это не похоже на задачу"}
            
            # Если есть уточняющие вопросы
            if result.get("questions") and len(result["questions"]) > 0:
                return {
                    "status": "questions_needed",
                    "questions": result["questions"],
                    "suggested_task": {
                        "title": result.get("title"),
                        "description": result.get("description"),
                        "priority": result.get("priority")
                    }
                }
            
            # Создаем задачу
            return {
                "status": "task_created",
                "task": {
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "priority": result.get("priority"),
                    "project_id": result.get("project_id"),
                    "deadline": result.get("deadline")
                }
            }
            
        except Exception as e:
            raise Exception(f"Ошибка анализа текста: {str(e)}")
    
    async def process_voice_message(self, audio_file_path: str, user_projects: List[Dict]) -> Dict[str, Any]:
        """Полный процесс: аудио → текст → анализ → задача"""
        try:
            # Шаг 1: Распознавание речи
            text = await self.transcribe_audio(audio_file_path)
            
            # Шаг 2: Анализ и создание задачи
            task_data = await self.analyze_text_request(text, user_projects)
            
            if task_data["status"] == "not_task":
                return {
                    "status": "not_task",
                    "original_text": text,
                    "message": "Это не похоже на задачу"
                }
            
            task_data["original_text"] = text
            return task_data
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "original_text": "Ошибка распознавания речи"
            }
