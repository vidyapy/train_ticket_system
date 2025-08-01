import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
    Boolean
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
    status = Column(SqlEnum(BookingStatus, native_enum=False), default=BookingStatus.WAITING, nullable=False)
    seats_booked = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships (optional but recommended)
    user = relationship("User", back_populates="bookings")
    train = relationship("Train", back_populates="bookings")
