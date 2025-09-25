import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.api_v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=0.1,
        )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    pass


app = FastAPI(
    title="Project Manager API",
    description="API для управления проектами с AI ассистентом",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
allowed_origins = [
    "https://projectmanager.chickenkiller.com"
]
if hasattr(settings, 'WEBAPP_URL') and settings.WEBAPP_URL:
    allowed_origins.append(settings.WEBAPP_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Project Manager API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
