from typing import Optional

from api.ddd.entity.i_equatable import IEquatable
from api.ddd.value_object.task_id import TaskId
from api.ddd.value_object.task_title import TaskTitle


class Task(IEquatable["Task"]):

    def __init__(self, title: TaskTitle, id: Optional[TaskId] = None, done: bool = False) -> None:
        if type(title) is not TaskTitle:
            raise ValueError("titleは必須です")
        if id is None:
            id = TaskId(None)
        self.__id: TaskId = id
        self.__title: TaskTitle = title
        self.__done: bool = done

    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        return self.__title
    
    @property
    def done(self):
        return self.__done

    def equals(self, other: "Task") -> bool:
        return self.id.value() == other.id.value()
    
    def change_title(self, title: TaskTitle) -> None:
        self.__title = title
