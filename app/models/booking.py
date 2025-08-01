import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SqlEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base  

class BookingStatus(enum.IntEnum):
    CONFIRMED = 1
    WAITING = 2
    TATKAL = 3
    CANCELLED = 4

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    train_id = Column(UUID(as_uuid=True), ForeignKey("trains.id"), nullable=False)

    seat_number = Column(Integer, nullable=True)
    booking_time = Column(DateTime, default=datetime.utcnow)

    status = Column(SqlEnum(BookingStatus, native_enum=False), default=BookingStatus.WAITING, nullable=False)

    # Relationships (optional but recommended)
    user = relationship("User", back_populates="bookings")
    train = relationship("Train", back_populates="bookings")
