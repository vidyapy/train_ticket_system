from fastapi import APIRouter

from app.api.endpoints.public import user as user_router

api_router = APIRouter()

api_router.include_router(user_router.router, prefix="/users", tags=["users"])