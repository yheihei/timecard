from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.domain.models.attendance_record.attendance_record import \
    AttendanceRecord
from api.domain.models.attendance_record.attendance_time import AttendanceTime
from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User
from api.infrastructure.sqlalchemy.clock_in.i_clock_in_repository import \
    IClockInRepository
from api.models.attendance_record import \
    AttendanceRecord as AttendanceRecordModel
from api.utils.custom_datetime import now


class ClockInRepository(IClockInRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_today_last_record(self, user: User) -> AttendanceRecord | None:
        """
        ユーザーの本日の最新の打刻を取得する
        """
        current = now()
        query = await self.db.execute(
            select(AttendanceRecordModel).where(
                AttendanceRecordModel.user_id == user.id,
                AttendanceRecordModel.timestamp >= current.replace(hour=0, minute=0, second=0, microsecond=0),
                AttendanceRecordModel.timestamp <= current,
            ).order_by(AttendanceRecordModel.timestamp.desc())
        )
        last_record: AttendanceRecordModel | None = query.scalars().first()
        if last_record is None:
            return None
        return AttendanceRecord(
            user=user,
            attendance_time=AttendanceTime(last_record.timestamp),
            type=last_record.type,
        )
    
    async def save(self, clock_in_record: ClockInRecord) -> None:
        """
        打刻を保存する
        """
        record = AttendanceRecordModel(
            user_id=clock_in_record.user.id,
            type=clock_in_record.type,
            timestamp=clock_in_record.attendance_time.value,
        )
        self.db.add(record)
        await self.db.commit()