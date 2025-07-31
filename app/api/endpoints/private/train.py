from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.session import SessionLocal
from app.crud import train as crud_train
from app.schemas.train import  TrainNameResponse

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/names", response_model=list[TrainNameResponse])
async def read_train_names(db: AsyncSession = Depends(get_db)):
    """Get all train names"""
    trains = await crud_train.get_train_names(db)
    return [{"id": train.id, "name": train.name} for train in trains]


