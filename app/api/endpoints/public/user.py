from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.crud import user as crud_user
from app.schemas.user import CreateUserRequest
from app.helpers.common import create_response

router = APIRouter()

@router.post("/create-user")
async def create_user(request_data: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    user = await crud_user.create_user(db, request_data)
    if user:
        return create_response(200, "User created successfully", user)
    return {"message": "User creation failed"}
