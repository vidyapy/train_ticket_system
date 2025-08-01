from pydantic import BaseModel
from datetime import datetime

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
