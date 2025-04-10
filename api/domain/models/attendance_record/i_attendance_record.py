import abc
import enum

from api.domain.models.attendance_record.attendance_time import AttendanceTime
from api.domain.models.user.user import User


class AttendanceType(enum.Enum):
    CLOCK_IN = "CLOCK_IN"
    CLOCK_OUT = "CLOCK_OUT"


class IAttendanceRecord(abc.ABC):

    @property
    @abc.abstractmethod
    def user(self) -> User:
        pass

    @property
    @abc.abstractmethod
    def attendance_time(self) -> AttendanceTime:
        pass

    @property
    @abc.abstractmethod
    def type(self) -> AttendanceType:
        pass
