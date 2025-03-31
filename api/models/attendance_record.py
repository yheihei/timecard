import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.base import TimestampMixin
from api.utils.custom_datetime import now


class AttendanceType(enum.Enum):
    CLOCK_IN = "clock_in"
    CLOCK_OUT = "clock_out"


class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = "attendance_record"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[AttendanceType] = mapped_column(Enum(AttendanceType), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
