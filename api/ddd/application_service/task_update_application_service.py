from api.ddd.repository.i_task_repository import ITaskRepository
from api.ddd.value_object import TaskTitle


class TaskUpdateApplicationService:
    def __init__(self, task_repository: ITaskRepository):
        self.__task_repository = task_repository

    async def update(self, task_id: int, task_name: str):
        task = await self.__task_repository.get_task(task_id)
        task.change_title(TaskTitle(task_name))
        return await self.__task_repository.save(task)