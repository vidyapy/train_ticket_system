from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class TrainNameResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class TrainCreateRequest(BaseModel):
    name: str
    source: str
    destination: str
    total_seats: int
    departure_time: datetime
    arrival_time: datetime

class TrainCreateResponse(BaseModel):
    id: UUID
    name: str
    source: str
    destination: str
    total_seats: int
    departure_time: datetime
    arrival_time: datetime
    
    class Config:
        from_attributes = True
