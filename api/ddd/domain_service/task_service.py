from api.ddd.repository.i_task_repository import ITaskRepository


class TaskService:
    def __init__(self, repository: ITaskRepository) -> None:
        self.repository: ITaskRepository = repository
