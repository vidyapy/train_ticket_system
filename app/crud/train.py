from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.train import Train


async def get_train_names(db: AsyncSession):
    """Get all train names and IDs"""
    result = await db.execute(select(Train.id, Train.name))
    return result.all()
