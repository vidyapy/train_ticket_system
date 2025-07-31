from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import CreateUserRequest, UserResponse
from app.models.user import User

async def create_user(db: AsyncSession, request_data: CreateUserRequest):
    """Create a new user in the database"""
    new_user = User(
        username=request_data.username,
        hashed_password=request_data.password,
        email=request_data.email,
        is_admin=request_data.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return True

