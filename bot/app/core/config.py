from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str
    WEBAPP_URL: str = "https://projectmanager.chickenkiller.com"
    BACKEND_URL: str = "https://projectmanager.chickenkiller.com"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорируем лишние переменные


settings = Settings()
