# app/api/routes/tatkal.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime
from sqlalchemy import select

from app.schemas.booking import TatkalRequest
from app.models.train import Train
from app.models.booking import Booking, BookingStatus
from app.helpers.common import is_tatkal_window_open
from app.models.user import User
from app.schemas.booking import TicketCreateResponse

router = APIRouter()

async def book_tatkal(
    db: AsyncSession,
    request_data: TatkalRequest,
    user: User
):
    result = await db.execute(select(Train).where(Train.id == request_data.train_id))
    train = result.scalar_one_or_none()

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    if not is_tatkal_window_open(train.departure_time):
        raise HTTPException(status_code=403, detail="Tatkal booking window is closed")

    if train.available_seats < request_data.seats:
        raise HTTPException(status_code=400, detail="Not enough seats available")

    booking = Booking(
        user_id=user.id,
        train_id=train.id,
        seats_booked=request_data.seats,
        status=BookingStatus.TATKAL,
        is_tatkal=True
    )

    train.available_seats -= request_data.seats
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return TicketCreateResponse(
        booking_id=booking.id,
        train_id=booking.train_id,
        user_id=booking.user_id,
        seats_booked=booking.seats_booked,
        status=booking.status,
        created_at=booking.created_at
    )
