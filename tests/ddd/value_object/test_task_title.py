
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.value_object.exception import ValueObjectError
from api.ddd.value_object.task_title import TaskTitle


class TestTaskTitle:

    @pytest.mark.asyncio
    async def test_create_title(self, db: AsyncSession, async_client):
        task_title = TaskTitle(name = "1")
        assert "1" == task_title.value()

    @pytest.mark.asyncio
    async def test_title_long_error(self, db: AsyncSession, async_client):
        with pytest.raises(ValueObjectError):
            task_title = TaskTitle(name = "a" * 256)

    @pytest.mark.asyncio
    async def test_title_short_error(self, db: AsyncSession, async_client):
        with pytest.raises(ValueObjectError):
            task_title = TaskTitle(name = None)
        with pytest.raises(ValueObjectError):
            task_title = TaskTitle(name = "")
