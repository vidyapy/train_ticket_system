# Train Endpoint Implementation Plan

## Overview
This document outlines the implementation plan for creating an endpoint to read train names in the Train Ticket Booking System.

## Current System Analysis
- FastAPI application with SQLAlchemy ORM
- Async database operations using aiosqlite
- Train model already exists with name field
- CRUD and API directories are currently empty
- Need to implement proper separation of concerns

## Implementation Steps

### 1. Create Train Schema (`app/schemas/train.py`)
Create Pydantic models for train data representation:
- `TrainBase`: Base model with common fields
- `TrainCreate`: Model for creating new trains
- `TrainUpdate`: Model for updating existing trains
- `Train`: Model for API responses with ID
- `TrainNameResponse`: Simplified model for just train names

### 2. Create Train CRUD Operations (`app/crud/train.py`)
Implement database operations:
- `get_train(db, train_id)`: Get a specific train by ID
- `get_trains(db, skip, limit)`: Get all trains with pagination
- `get_train_names(db)`: Get just train names (for our specific requirement)
- `create_train(db, train)`: Create a new train
- `update_train(db, db_train, train)`: Update an existing train
- `delete_train(db, train_id)`: Delete a train

### 3. Create Train API Endpoints (`app/api/v1/train.py`)
Implement the API routes:
- `GET /trains/`: Get all trains
- `GET /trains/names`: Get just train names (our specific requirement)
- `GET /trains/{train_id}`: Get a specific train
- `POST /trains/`: Create a new train
- `PUT /trains/{train_id}`: Update a train
- `DELETE /trains/{train_id}`: Delete a train

### 4. Register API Endpoints (`app/api/v1/__init__.py`)
Create API router and register train endpoints.

### 5. Update Main Application (`app/main.py`)
Mount the API router to the main application.

## Detailed Implementation

### Train Schema Models
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrainBase(BaseModel):
    name: str
    total_seats: int
    available_seats: int
    departure_time: datetime
    arrival_time: datetime

class TrainCreate(TrainBase):
    pass

class TrainUpdate(TrainBase):
    name: Optional[str] = None
    total_seats: Optional[int] = None
    available_seats: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None

class Train(TrainBase):
    id: int
    
    class Config:
        from_attributes = True

class TrainNameResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
```

### Train CRUD Operations
```python
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.train import Train
from app.schemas.train import TrainCreate, TrainUpdate

async def get_train_names(db: AsyncSession):
    result = await db.execute(select(Train.id, Train.name))
    return result.all()

async def get_trains(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Train).offset(skip).limit(limit))
    return result.scalars().all()

async def get_train(db: AsyncSession, train_id: int):
    result = await db.execute(select(Train).where(Train.id == train_id))
    return result.scalar_one_or_none()

async def create_train(db: AsyncSession, train: TrainCreate):
    db_train = Train(**train.dict())
    db.add(db_train)
    await db.commit()
    await db.refresh(db_train)
    return db_train

async def update_train(db: AsyncSession, db_train: Train, train: TrainUpdate):
    update_data = train.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_train, key, value)
    await db.commit()
    await db.refresh(db_train)
    return db_train

async def delete_train(db: AsyncSession, train_id: int):
    result = await db.execute(select(Train).where(Train.id == train_id))
    db_train = result.scalar_one_or_none()
    if db_train:
        await db.delete(db_train)
        await db.commit()
    return db_train
```

### Train API Endpoints
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.session import SessionLocal
from app.crud import train as crud_train
from app.schemas.train import Train, TrainCreate, TrainUpdate, TrainNameResponse

router = APIRouter(prefix="/trains", tags=["trains"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/names", response_model=list[TrainNameResponse])
async def read_train_names(db: AsyncSession = Depends(get_db)):
    trains = await crud_train.get_train_names(db)
    return [{"id": train.id, "name": train.name} for train in trains]

@router.get("/", response_model=list[Train])
async def read_trains(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    trains = await crud_train.get_trains(db, skip=skip, limit=limit)
    return trains

@router.get("/{train_id}", response_model=Train)
async def read_train(train_id: int, db: AsyncSession = Depends(get_db)):
    db_train = await crud_train.get_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(status_code=404, detail="Train not found")
    return db_train

@router.post("/", response_model=Train)
async def create_train(train: TrainCreate, db: AsyncSession = Depends(get_db)):
    return await crud_train.create_train(db=db, train=train)

@router.put("/{train_id}", response_model=Train)
async def update_train(
    train_id: int, train: TrainUpdate, db: AsyncSession = Depends(get_db)
):
    db_train = await crud_train.get_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(status_code=404, detail="Train not found")
    return await crud_train.update_train(db=db, db_train=db_train, train=train)

@router.delete("/{train_id}")
async def delete_train(train_id: int, db: AsyncSession = Depends(get_db)):
    db_train = await crud_train.get_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(status_code=404, detail="Train not found")
    await crud_train.delete_train(db=db, train_id=train_id)
    return {"message": "Train deleted successfully"}
```

## Testing the Implementation
After implementation, we should test:
1. The new endpoint `/trains/names` returns a list of train names
2. The existing functionality remains unaffected
3. Error handling works correctly
4. Database operations work as expected

## Next Steps
1. Switch to Code mode to implement the solution
2. Create the schema file
3. Create the CRUD operations
4. Create the API endpoints
5. Register the endpoints in the main application
6. Test the implementation