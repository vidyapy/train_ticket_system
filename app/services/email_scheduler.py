from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone, timedelta
from app.core.session import SessionLocal

from app.models.train import Train
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.helpers.email import send_email



async def send_reminder_emails():
    async with SessionLocal() as db:
        now = datetime.utcnow()  # Use timezone-naive datetime to match database schema
        target_time = now + timedelta(minutes=30)

        result = await db.execute(
            select(Train).where(Train.departure_time.between(target_time, target_time + timedelta(minutes=1)))
        )
        trains_departing_soon = result.scalars().all()

        for train in trains_departing_soon:
            booking_result = await db.execute(
                select(Booking).where(
                    Booking.train_id == train.id,
                    Booking.status == BookingStatus.CONFIRMED
                )
            )
            bookings = booking_result.scalars().all()

            for booking in bookings:
                user_result = await db.execute(select(User).where(User.id == booking.user_id))
                user = user_result.scalar_one_or_none()
                if user:
                    message = (
                        f"Dear Passenger,\n\n"
                        f"This is a reminder that your train (Name: {train.name}) departs at {train.departure_time}.\n"
                        f"Your seat details: {booking.seats_booked}\n\n"
                        f"Have a safe journey!"
                    )
                    await send_email(user.email, "Train Departure Reminder", message)

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder_emails, "interval", minutes=1)
    scheduler.start()
