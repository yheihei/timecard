
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.entity.task import Task
from api.ddd.value_object.task_id import TaskId
from api.ddd.value_object.task_title import TaskTitle


class TestTask:

    @pytest.mark.asyncio
    async def test_create(self, db: AsyncSession, async_client):
        Task(TaskTitle("タスクの名前"), TaskId(1))

    @pytest.mark.asyncio
    async def test_equals(self, db: AsyncSession, async_client):
        task1 = Task(TaskTitle("タスクの名前"), TaskId(1))
        task2 = Task(TaskTitle("タスクの名前"), TaskId(2))
        assert True == task1.equals(task1)
        assert False == task1.equals(task2)
