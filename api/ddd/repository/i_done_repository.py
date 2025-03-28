from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class IDoneRepository(ABC):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def create(self, task_id: int) -> None:
        pass
