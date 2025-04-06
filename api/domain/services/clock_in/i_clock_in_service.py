import abc

from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User
from api.infrastructure.sqlalchemy.clock_in.i_clock_in_repository import \
    IClockInRepository


class IClockInService(abc.ABC):
    @abc.abstractmethod
    def __init__(self, clock_in_repository) -> IClockInRepository:
        pass

    @abc.abstractmethod
    def clock_in(self, clock_in_record: ClockInRecord) -> None:
        """Clock in the user."""
        pass

    @abc.abstractmethod
    def is_already_clocked_in(self, user: User) -> bool:
        """Check if the user is already clocked in."""
        pass