from typing import List, Tuple

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.main import app


class TestCreateActivity:

    async def get_token(self, async_client):
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
        return response.json().get("access_token")

    @pytest.mark.asyncio
    async def test_create(self, db: AsyncSession, async_client):
        token = await self.get_token(async_client)
        response = await async_client.post(
            "/users/1/activities",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(response.json())
