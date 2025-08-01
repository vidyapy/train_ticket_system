from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from uuid import UUID

from app.core.dependencies import get_db
from app.schemas.booking import BookTrainRequest, BookingID
from app.crud import booking as crud_booking
from app.helpers.common import create_response
from app.core.dependencies import get_current_user
from app.models.user import User 

router = APIRouter()


@router.post("/book_ticket")
async def book_ticket(
    ticket_data: BookTrainRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    result = await crud_booking.book_ticket(db, ticket_data, current_user)
    if result:
        return create_response(201, "Ticket booked successfully", result)
    raise HTTPException(status_code=400, detail="Ticket booking failed")

@router.post("/cancel_ticket")
async def cancel_ticket(
    request_data: BookingID,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Cancel a booked ticket"""
    result = await crud_booking.cancel_ticket(db, request_data.booking_id, current_user)
    if result:
        return create_response(200, "Ticket cancelled successfully", result)
    raise HTTPException(status_code=404, detail="Booking not found or cancellation failed")
