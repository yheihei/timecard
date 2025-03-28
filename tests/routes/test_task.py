from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model


class TestTask:
    """
    tasks関連のエンドポイントのテスト
    """

    @pytest.mark.asyncio
    async def test_create_task(self, db: AsyncSession, async_client):
        response = await async_client.post(
            "/tasks", json={"title": "foo",}
        )
        result: Result = await db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done).filter(task_model.Task.title == "foo")
        )
        tasks: List[Tuple] = result.all()
        assert 1 == len(tasks)
        assert (1, "foo", False) == tasks[0]

    @pytest.mark.asyncio
    async def test_get_tasks(self, db, async_client):
        # タスク生成
        for i in range(0, 2):
            task = task_model.Task(title=f"{i+1}")
            db.add(task)
            await db.commit()
            await db.refresh(task)

        response = await async_client.get(
            "/tasks",
        )
        assert [
            {"title": "1", "id": 1, "done": False},
            {"title": "2", "id": 2, "done": False}
        ] == response.json()

    @pytest.mark.asyncio
    async def test_update_task(self, db: AsyncSession, async_client):
        # タスク生成
        created_task = task_model.Task(title=f"1")
        db.add(created_task)
        await db.commit()
        await db.refresh(created_task)

        res = await async_client.put(
            "/tasks/1", json={"title": "1modified"}
        )

        result: Result = await db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
            ).where(task_model.Task.id == created_task.id)
        )
        assert (created_task.id, "1modified") == result.first()

    @pytest.mark.asyncio
    async def test_done_task(self, db: AsyncSession, async_client):
        # タスク生成
        created_task = task_model.Task(title=f"1")
        db.add(created_task)
        await db.commit()
        await db.refresh(created_task)

        res = await async_client.put(
            "/tasks/1/done",
        )
        # 関連テーブルが更新されたためもう一度取得
        await db.refresh(created_task)

        result: Result = await db.execute(
            select(
                task_model.Done.id,
            ).where(task_model.Done.id == created_task.id)
        )
        assert (created_task.id,) == result.first()