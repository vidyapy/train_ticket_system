from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from uuid import UUID
from app.models.booking import Booking, BookingStatus
from datetime import datetime
from fastapi import HTTPException

from app.schemas.booking import BookTrainRequest, TicketCreateResponse
from app.models.train import Train
from app.models.user import User


async def book_ticket(db: AsyncSession, request_data: BookTrainRequest, user: User):

    result = await db.execute(select(Train).where(Train.id == request_data.train_id))
    train = result.scalar_one_or_none()

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    if train.available_seats >= request_data.seats_requested:
        status = BookingStatus.CONFIRMED
        train.available_seats -= request_data.seats_requested
    else:
        status = BookingStatus.WAITING

    booking = Booking(
        user_id=user.id,
        train_id=request_data.train_id,
        seats_booked=request_data.seats_requested,
        status=status
    )

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

async def cancel_ticket(db: AsyncSession, booking_id: UUID, user: User):
    
    
    result = await db.execute(
        select(Booking).where(
            Booking.id == booking_id, 
            Booking.user_id == user.id)
        )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == BookingStatus.CONFIRMED:
        train_result = await db.execute(select(Train).where(Train.id == booking.train_id))
        train = train_result.scalar_one_or_none()
        if train:
            train.available_seats += booking.seats_booked

    await db.delete(booking)
    await db.commit()

    # Check waiting list
    waiting_bookings = await db.execute(
        select(Booking).where(
            Booking.train_id == booking.train_id,
            Booking.status == BookingStatus.WAITING
        ).order_by(Booking.created_at)
    )
    waiting_booking = waiting_bookings.scalars().first()
    if waiting_booking:
        waiting_booking.status = BookingStatus.CONFIRMED
        train.available_seats -= waiting_booking.seats_booked
        await db.commit()
        await db.refresh(waiting_booking)
    return True    






