from api.ddd.entity.task import Task
from api.ddd.repository.i_task_repository import ITaskRepository
from api.ddd.value_object.task_title import TaskTitle


class TaskCreateApplicationService:

    def __init__(self, repository: ITaskRepository) -> None:
        self.repository: ITaskRepository = repository

    async def register(self, title: str) -> Task:
        task = Task(title=TaskTitle(title))
        return await self.repository.create(task)