from fastapi import APIRouter
from app.api.api_v1.endpoints import tasks, projects, users, ai, photos, admin

api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
