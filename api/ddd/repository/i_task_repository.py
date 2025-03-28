from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.entity.task import Task
from api.ddd.value_object import TaskId, TaskTitle


class ITaskRepository(ABC):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def create(self, task_entity: Task) -> Task:
        pass

    @abstractmethod
    async def get_tasks_with_done(self) -> list[Task]:
        return [Task(TaskTitle("title1"), TaskId(1), False), Task(TaskTitle("title2"), TaskId(2), False)]

    @abstractmethod
    async def get_task(self, id: int) -> Task:
        return Task(TaskTitle("title1"), TaskId(1), False)

    @abstractmethod
    async def save(self, task: Task) -> Task:
        return task
