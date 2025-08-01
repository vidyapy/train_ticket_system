from fastapi import APIRouter

from app.api.endpoints.private import train as train_router
from app.api.endpoints.private import booking as booking_router

api_router = APIRouter()


api_router.include_router(train_router.router, prefix="/trains", tags=["trains"])
api_router.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
