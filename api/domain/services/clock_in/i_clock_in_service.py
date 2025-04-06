import abc

from api.domain.models.clock_in.clock_in_record import ClockInRecord
from api.domain.models.user.user import User


class IClockInService(abc.ABC):
    @abc.abstractmethod
    def __init__(self, clock_in_repository):
        pass

    @abc.abstractmethod
    async def clock_in(self, clock_in_record: ClockInRecord) -> ClockInRecord:
        """Clock in the user."""

    @abc.abstractmethod
    async def is_already_clocked_in(self, user: User) -> bool:
        """Check if the user is already clocked in."""
