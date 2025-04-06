import abc

from api.domain.models.attendance_record.attendance_record import \
    AttendanceRecord
from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User


class IClockInRepository:
    @abc.abstractmethod
    async def get_today_last_record(self, user: User) -> AttendanceRecord | None:
        """
        ユーザーの最新の打刻を取得する
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, clock_in_record: ClockInRecord) -> None:
        """
        打刻を保存する
        """
        raise NotImplementedError