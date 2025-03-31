from typing import AsyncGenerator, List, Tuple

import pytest
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.auth import crud
from api.auth.auth_api import get_current_user
from api.auth.crud import get_user_by_username
from api.db import get_db
from api.main import app
from api.models import User
from api.models.attendance_record import AttendanceRecord, AttendanceType
from api.utils.custom_datetime import now


class TestCreateActivity:

    async def get_token(self, async_client) -> Tuple[User, str]:
        """
        Create a user and get a token
        """
        response = await async_client.post(
            "/users",
            json={
                "email": "hoge@example.com",
                "username": "hogehoge",
                "password": "fugafuga",
            },
        )
        user_id = response.json().get("id")
        response = await async_client.post(
            "/token",
            data={
                "username": "hogehoge",
                "password": "fugafuga",
            },
        )
        access_token = response.json().get("access_token")
        return user_id, access_token

    @pytest.mark.freeze_time("2024-03-03T09:00:00+09:00")
    @pytest.mark.asyncio
    async def test_create(self, test_async_generator: AsyncGenerator[AsyncClient, AsyncSession]):
        client, db = test_async_generator
        user_id, access_token = await self.get_token(client)

        response = await client.post(
            f"/users/{user_id}/attendance-records",
            headers={"Authorization": f"Bearer {access_token}"},
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
        assert attendance_record.user_id == user_id
        assert str(attendance_record.timestamp) == "2024-03-03 09:00:00"
