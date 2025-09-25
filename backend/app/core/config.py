from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str
    WEBAPP_URL: str = "https://projectmanager.chickenkiller.com"
    BACKEND_URL: str = "https://projectmanager.chickenkiller.com"
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "project_manager"
    DB_USER: str = "postgres"
    DB_PASS: str = "password"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "development"
    
    @property
    def database_url(self) -> str:
        # Используем SQLite для простоты разработки
        return "sqlite:///./project_manager.db"
        # Для PostgreSQL раскомментируйте строку ниже:
        # return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"


settings = Settings()
