from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import CreateUserRequest, UserResponse, LoginRequest
from app.models.user import User
from app.helpers.security import hash_password, verify_password


async def create_user(db: AsyncSession, request_data: CreateUserRequest):
    """Create a new user in the database"""

    hashed_pwd = hash_password(request_data.password)

    new_user = User(
        username=request_data.username,
        hashed_password=hashed_pwd,
        email=request_data.email,
        is_admin=request_data.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return True

async def authenticate_user(db: AsyncSession, request_data: LoginRequest):
    """Authenticate user by username and password"""
    
    query = select(User).where(User.username == request_data.username, User.is_deleted == False)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user and verify_password(request_data.password, user.hashed_password):
        return user
    return None

