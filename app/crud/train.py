from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.train import Train
from app.models.user import User
from app.schemas.train import TrainCreateRequest


async def get_train_names(db: AsyncSession):
    """Get all train names and IDs"""
    result = await db.execute(select(Train.id, Train.name))
    return result.all()

async def create_train(db: AsyncSession, train_data: TrainCreateRequest, user: User):

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create trains"
        )

    new_train = Train(
        name=train_data.name,
        source=train_data.source,
        destination=train_data.destination,
        total_seats=train_data.total_seats,
        available_seats=train_data.total_seats,
        departure_time=train_data.departure_time,
        arrival_time=train_data.arrival_time
    )
    db.add(new_train)
    await db.commit()
    await db.refresh(new_train)
    return new_train
