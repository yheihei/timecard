from datetime import datetime


class AttendanceTime:
    def __init__(self, timestamp: datetime) -> None:
        self.__timestamp: datetime = timestamp

    @property
    def value(self) -> datetime:
        return self.__timestamp