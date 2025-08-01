from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.core.dependencies import get_db
from app.crud import train as crud_train
from app.schemas.train import TrainNameResponse, TrainCreateRequest
from app.helpers.common import create_response
from app.core.dependencies import get_current_user
from app.models.user import User 

router = APIRouter()


@router.get("/names", response_model=list[TrainNameResponse])
async def read_train_names(db: AsyncSession = Depends(get_db)):
    """Get all train names"""
    trains = await crud_train.get_train_names(db)
    return [{"id": train.id, "name": train.name} for train in trains]

@router.post("/create_train")
async def create_train(
    train_data: TrainCreateRequest, 
    db: AsyncSession = Depends(get_db), 
    current_user: Any = Depends(get_current_user)
):
    """Create a new train"""
    train = await crud_train.create_train(db, train_data, current_user)
    if train:
        return create_response(201, "Train created successfully", train)

    raise HTTPException(status_code=400, detail="Train creation failed")


