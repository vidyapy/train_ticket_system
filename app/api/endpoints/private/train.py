from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.crud import train as crud_train
from app.schemas.train import TrainNameResponse

router = APIRouter()


@router.get("/names", response_model=list[TrainNameResponse])
async def read_train_names(db: AsyncSession = Depends(get_db)):
    """Get all train names"""
    trains = await crud_train.get_train_names(db)
    return [{"id": train.id, "name": train.name} for train in trains]


