from sqlalchemy.ext.asyncio import AsyncSession
from app.core.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.helpers.common import get_user_by_id
from app.core.config import get_settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  


async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with SessionLocal() as session:
        yield session


settings = get_settings()

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub") 
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(user_id, db)  
    if user is None:
        raise credentials_exception

    return user
