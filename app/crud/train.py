from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.train import Train
from app.models.user import User
from app.schemas.train import TrainCreateRequest, TrainCreateResponse


async def view_train(db: AsyncSession, user: User):
    """Get all train names and IDs"""
    result = await db.execute(select(Train))
    trains = result.scalars().all()

    train_list = []
    for train in trains:
        waiting_list = max(train.total_seats - train.available_seats, 0)
        train_list.append({
            "id": train.id,
            "name": train.name,
            "source": train.source,
            "destination": train.destination,
            "departure_time": train.departure_time,
            "arrival_time": train.arrival_time,
            "total_seats": train.total_seats,
            "available_seats": train.available_seats,
            "waiting_list_count": waiting_list
        })

    return train_list


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
    result = TrainCreateResponse(
        id=new_train.id,
        name=new_train.name,
        source=new_train.source,
        destination=new_train.destination,
        total_seats=new_train.total_seats, 
        departure_time=new_train.departure_time,
        arrival_time=new_train.arrival_time
    ) 
    return result
