from sqlalchemy.ext.asyncio import AsyncSession
from app.core.session import SessionLocal


async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with SessionLocal() as session:
        yield session