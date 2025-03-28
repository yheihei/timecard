
import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
from api.ddd.repository import DoneRepository


class TestDoneRepository:

    @pytest.mark.asyncio
    async def test_mark_as_done(self, db, async_client):
        # タスク生成
        created_task = task_model.Task(title="task1")
        db.add(created_task)
        await db.commit()
        await db.refresh(created_task)
        created_task.id

        await DoneRepository(db).create(created_task.id)
        # 関連テーブルが更新されたためもう一度取得
        await db.refresh(created_task)

        # doneが作成されていること
        result: Result = await db.execute(
            select(task_model.Done.id).filter(task_model.Done.id == created_task.id)
        )       
        dones = result.all()
        assert 1 == len(dones)
        assert (created_task.id,) == dones[0]
