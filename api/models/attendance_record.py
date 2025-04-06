import enum

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from api.db import Base
from api.models.base import TimestampMixin
from api.utils.custom_datetime import now


class AttendanceType(enum.Enum):
    CLOCK_IN = "CLOCK_IN"
    CLOCK_OUT = "CLOCK_OUT"


class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = "attendance_record"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    type: Mapped[AttendanceType] = mapped_column(Enum(AttendanceType), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
