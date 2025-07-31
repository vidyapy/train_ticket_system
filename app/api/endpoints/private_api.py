from fastapi import APIRouter

from app.api.endpoints.private import train as train_router

api_router = APIRouter()


api_router.include_router(train_router.router, prefix="/trains", tags=["trains"])
