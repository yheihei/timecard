from api.ddd.repository.i_done_repository import IDoneRepository


class DoneCreateApplicationService:

    def __init__(self, repository: IDoneRepository) -> None:
        self.repository: IDoneRepository = repository

    async def register(self, task_id: int) -> None:
        await self.repository.create(task_id)