from fastapi import APIRouter
from app.api.endpoints import private_api, public_api

api_router = APIRouter()

api_router.include_router(private_api.api_router, prefix="/private", tags=["private"])
# api_router.include_router(public_api.api_router, prefix="/public", tags=["public"])