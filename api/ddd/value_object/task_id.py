from typing import Optional


class TaskId:
    def __init__(self, id: Optional[int]) -> None:
        self.__id: Optional[int] = id

    @property
    def id(self) -> Optional[int]:
        return self.__id

    def value(self) -> Optional[int]:
        return self.__id
