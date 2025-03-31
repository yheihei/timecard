from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.auth import crud
from api.auth.auth_api import get_current_user
from api.auth.crud import get_user_by_username
from api.main import app
from api.models import User
from api.models.attendance_record import AttendanceRecord, AttendanceType
from api.utils.custom_datetime import now


class TestCreateActivity:

    async def get_token(self, db: AsyncSession, async_client) -> Tuple[User, str]:
        """
        Create a user and get a token
        """
        await async_client.post(
            "/users",
            json={
                "email": "hoge@example.com",
                "username": "hogehoge",
                "password": "fugafuga",
            },
        )
        response = await async_client.post(
            "/token",
            data={
                "username": "hogehoge",
                "password": "fugafuga",
            },
        )
        return (
            await crud.get_user_by_username(db, username="hogehoge"),
            response.json().get("access_token"),
        )

    @pytest.mark.asyncio
    async def test_create(self, db: AsyncSession, async_client):
        user, token = await self.get_token(db, async_client)
        user_id = user.id
        response = await async_client.post(
            f"/users/{user.id}/attendance-records",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "type": "CLOCK_IN",
            },
        )

        assert response.status_code == 200

        # AttendanceRecordが作成されていることを確認
        result = await db.execute(
            select(AttendanceRecord).filter(
                AttendanceRecord.user_id == user_id,
                AttendanceRecord.type == "CLOCK_IN",
            )
        )
        attendance_record: AttendanceRecord | None = result.scalars().first()
        assert attendance_record is not None
        assert attendance_record.type == AttendanceType.CLOCK_IN
