import openai
from typing import Optional, Dict, Any
from app.core.config import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


async def transcribe_audio(audio_file_path: str) -> str:
    """Преобразование голосового сообщения в текст"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        raise Exception(f"Ошибка распознавания речи: {str(e)}")


async def analyze_task_request(text: str, user_projects: list) -> Dict[str, Any]:
    """Анализ текста и создание структурированной задачи"""
    projects_info = "\n".join([f"- {p['name']} (ID: {p['id']})" for p in user_projects])
    
    prompt = f"""
Проанализируй следующий текст и создай структурированную задачу:

Текст: "{text}"

Доступные проекты пользователя:
{projects_info}

Верни ответ в JSON формате:
{{
    "title": "Краткое название задачи",
    "description": "Подробное описание",
    "project_id": ID_проекта_или_null,
    "priority": "low|medium|high|urgent",
    "deadline": "YYYY-MM-DD HH:MM" или null,
    "questions": ["список уточняющих вопросов если нужно"]
}}

Правила:
1. Если проект не указан, project_id = null
2. Если дедлайн не указан, deadline = null
3. Если нужны уточнения, добавь вопросы в массив
4. Приоритет определяй по ключевым словам: "срочно", "важно", "не важно"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты AI ассистент для создания задач. Отвечай только в JSON формате."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Ошибка анализа текста: {str(e)}")


async def generate_task_from_audio(audio_file_path: str, user_projects: list) -> Dict[str, Any]:
    """Полный процесс: аудио → текст → анализ → задача"""
    # Шаг 1: Распознавание речи
    text = await transcribe_audio(audio_file_path)
    
    # Шаг 2: Анализ и создание задачи
    task_data = await analyze_task_request(text, user_projects)
    task_data["original_text"] = text
    
    return task_data
