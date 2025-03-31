import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from api.db import Base
from api.models.base import TimestampMixin
from api.utils.custom_datetime import now


class AttendanceType(enum.Enum):
    CLOCK_IN = "clock_in"
    CLOCK_OUT = "clock_out"


class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = "attendance_record"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(AttendanceType), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=now, nullable=False)
