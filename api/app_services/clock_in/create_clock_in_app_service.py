
from api.domain.models.attendance_record.attendance_time import AttendanceTime
from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User
from api.domain.services.clock_in.exceptions import AlreadyClockedInError
from api.domain.services.clock_in.i_clock_in_service import IClockInService


class CreateClockInAppService:
    def __init__(self, clock_in_service: IClockInService):
        self.__clock_in_service = clock_in_service

    async def execute(self, user: User, attendance_time: AttendanceTime) -> ClockInRecord:
        if await self.__clock_in_service.is_already_clocked_in(user):
            raise AlreadyClockedInError("User is already clocked in.")
        return await self.__clock_in_service.clock_in(
            ClockInRecord(user, attendance_time)
        )
