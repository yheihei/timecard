from datetime import datetime

from api.domain.models.attendance_record.i_attendance_record import (
    AttendanceType, IAttendanceRecord)
from api.domain.models.user.user import User


class AttendanceRecord(IAttendanceRecord):
    def __init__(self, user: User, timestamp: datetime, type: AttendanceType):
        self.__user = user
        self.__timestamp = timestamp
        self.__type = type

    @property
    def user(self) -> User:
        return self.__user

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def type(self) -> AttendanceType:
        return self.__type