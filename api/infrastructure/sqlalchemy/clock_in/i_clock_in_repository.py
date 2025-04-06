import abc

from api.domain.models.attendance_record.attendance_record import \
    AttendanceRecord
from api.domain.models.user.user import User


class IClockInRepository:
    def get_last_record(self, user: User) -> AttendanceRecord | None:
        """
        ユーザーの最新の打刻を取得する
        """
        raise NotImplementedError