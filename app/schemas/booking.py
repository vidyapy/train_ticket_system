from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class BookTrainRequest(BaseModel):
    train_id: UUID
    seats_requested: int

class TicketCreateResponse(BaseModel):
    booking_id: UUID
    train_id: UUID
    user_id: UUID
    seats_booked: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
        

class BookingID(BaseModel):
    booking_id: UUID

