from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.crud import user as crud_user
from app.schemas.user import CreateUserRequest, LoginRequest, LoginResponse
from app.helpers.common import create_response
from app.core.auth import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/create-user")
async def create_user(request_data: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    user = await crud_user.create_user(db, request_data)
    if user:
        return create_response(200, "User created successfully", user)
    raise HTTPException(status_code=400, detail="User creation failed")


@router.post("/login")
async def login_user(request_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud_user.authenticate_user(db, request_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": str(user.id), "username": user.username}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    user_data =  LoginResponse(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token
    )
    return create_response(200, "Login successful", user_data)

