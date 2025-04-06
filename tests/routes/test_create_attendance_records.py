from typing import AsyncGenerator, Tuple, TypedDict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from api.models.attendance_record import AttendanceRecord, AttendanceType

from .test_create_attendance_records_data import AttendanceRecordFactory


class TestCreateAttendanceRecords:

    class CreateTestUserParam(TypedDict):
        email: str
        username: str
        password: str

    async def create_user_and_get_token(self, async_client, create_user_param: CreateTestUserParam) -> Tuple[User, str]:
        """
        テスト用のユーザーを作成し、アクセストークンを取得する
        """
        response = await async_client.post(
            "/users",
            json={
                "email": create_user_param["email"],
                "username": create_user_param["username"],
                "password": create_user_param["password"],
            },
        )
        user_id = response.json().get("id")
        response = await async_client.post(
            "/token",
            data={
                "username": create_user_param["username"],
                "password": create_user_param["password"],
            },
        )
        access_token = response.json().get("access_token")
        return user_id, access_token

    @pytest.mark.freeze_time("2024-03-03T09:00:00+09:00")
    @pytest.mark.asyncio
    async def test_打刻操作をしたときの時刻で打刻が記録されること(self, test_async_generator: AsyncGenerator[AsyncClient, AsyncSession]):
        client, db = test_async_generator
        user_id, access_token = await self.create_user_and_get_token(
            client,
            {
                "email": "hogehoge@example.com",
                "username": "hogehoge",
                "password": "password",
            },
        )

        response = await client.post(
            f"/clock_in",
            headers={"Authorization": f"Bearer {access_token}"},
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
        assert str(attendance_record.timestamp) == "2024-03-03 09:00:00"

    @pytest.mark.asyncio
    async def test_未認証だと打刻できないこと(self, test_async_generator: AsyncGenerator[AsyncClient, AsyncSession]):
        client, db = test_async_generator

        response = await client.post(
            f"/clock_in",
            headers={"Authorization": f"Bearer fuga"},
        )

        assert response.status_code == 401

    @pytest.mark.freeze_time("2024-03-03T09:00:00+09:00")
    @pytest.mark.asyncio
    async def test_出勤打刻が当日内で連続したらエラーとなること(self, test_async_generator: AsyncGenerator[AsyncClient, AsyncSession]):
        client, db = test_async_generator
        user_id, access_token = await self.create_user_and_get_token(
            client,
            {
                "email": "hogehoge@example.com",
                "username": "hogehoge",
                "password": "password",
            },
        )

        # 当日内に出勤打刻を作る
        AttendanceRecordFactory._meta.sqlalchemy_session = db
        await AttendanceRecordFactory.create(
            user_id=user_id,
            type=AttendanceType.CLOCK_IN,
            timestamp="2024-03-03T06:00:00+09:00",
            created_at="2024-03-03T06:00:00+09:00",
            updated_at="2024-03-03T06:00:00+09:00",
        )

        response = await client.post(
            f"/clock_in",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "2連続で出勤打刻はできません"}
