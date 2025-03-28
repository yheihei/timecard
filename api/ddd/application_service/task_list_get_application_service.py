from typing import List

from api.ddd.entity.task import Task
from api.ddd.repository.i_task_repository import ITaskRepository


class TaskListGetApplicationService:

    def __init__(self, repository: ITaskRepository) -> None:
        self.repository: ITaskRepository = repository

    async def get(self) -> List[Task]:
        return await self.repository.get_tasks_with_done()