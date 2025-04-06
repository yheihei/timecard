from datetime import datetime

from api.domain.models.attendance_record.i_attendance_record import (
    AttendanceType, IAttendanceRecord)
from api.domain.models.user.user import User


class ClockInRecord(IAttendanceRecord):
    def __init__(self, user: User, timestamp: datetime):
        self.__user: User = user
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user
    
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @property
    def type(self) -> AttendanceType:
        return AttendanceType.CLOCK_IN
