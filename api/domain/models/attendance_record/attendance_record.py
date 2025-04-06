
from api.domain.models.attendance_record.attendance_time import AttendanceTime
from api.domain.models.attendance_record.i_attendance_record import (
    AttendanceType, IAttendanceRecord)
from api.domain.models.user.user import User


class AttendanceRecord(IAttendanceRecord):
    def __init__(self, user: User, attendance_time: AttendanceTime, type: AttendanceType):
        self.__user = user
        self.__attendance_time = attendance_time
        self.__type = type

    @property
    def user(self) -> User:
        return self.__user

    @property
    def attendance_time(self) -> AttendanceTime:
        return self.__attendance_time

    @property
    def type(self) -> AttendanceType:
        return self.__type