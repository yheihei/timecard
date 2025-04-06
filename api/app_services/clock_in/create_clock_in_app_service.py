from datetime import datetime

from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User
from api.domain.services.clock_in.exceptions import AlreadyClockedInError
from api.domain.services.clock_in.i_clock_in_service import IClockInService
from api.infrastructure.sqlalchemy.clock_in.i_clock_in_repository import \
    IClockInRepository


class CreateClockInAppService:
    def __init__(self, clock_in_repo: IClockInRepository, clock_in_service: IClockInService):
        self.__clock_in_repo = clock_in_repo
        self.__clock_in_service = clock_in_service

    def execute(self, user: User, clock_in_time: datetime):
        if self.__clock_in_service.is_already_clocked_in(user):
            raise AlreadyClockedInError("User is already clocked in.")
        return self.__clock_in_service.clock_in(
            ClockInRecord(user, clock_in_time)
        )
