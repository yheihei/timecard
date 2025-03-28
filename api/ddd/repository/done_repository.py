from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
from api.ddd.repository.i_done_repository import IDoneRepository


class DoneRepository(IDoneRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, task_id: int) -> None:
        # doneがあるか確認
        result: Result = await self.db.execute(
            select(task_model.Done).filter(task_model.Done.id == task_id)
        )
        done: Optional[Tuple[task_model.Done]] = result.first()
        # doneがすでにあった場合はエラー
        if done:
            raise ValueError(f"done already exists. task_id: {task_id}")
        # doneを作成
        done = task_model.Done(id=task_id)
        self.db.add(done)
        await self.db.commit()
        await self.db.refresh(done)
    
    # def __to_fastapi_model(self, task_entity: Task) -> task_model.Task:
    #     return task_model.Task(id=task_entity.id.value(), title=task_entity.title.value())
    
    # def __to_entity(self, task_data_model: task_model.Task, done: bool) -> Task:
    #     task_id = TaskId(int(task_data_model.id))
    #     task_title = TaskTitle(str(task_data_model.title))
    #     return Task(id=task_id, title=task_title, done=done)
