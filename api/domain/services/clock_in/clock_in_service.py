from api.domain.models.attendance_record.i_attendance_record import \
    AttendanceType
from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User
from api.domain.services.clock_in.exceptions import AlreadyClockedInError
from api.domain.services.clock_in.i_clock_in_service import IClockInService
from api.infrastructure.sqlalchemy.clock_in.i_clock_in_repository import \
    IClockInRepository


class ClockInService(IClockInService):
    def __init__(self, clock_in_repository: IClockInRepository):
        self.clock_in_repository = clock_in_repository

    def clock_in(self, clock_in_record: ClockInRecord):
        pass

    def is_already_clocked_in(self, user: User) -> bool:
        if last_record := self.clock_in_repository.get_last_record(user) is None:
            return False
        return last_record.type == AttendanceType.CLOCK_IN

