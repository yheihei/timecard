from typing import List, Tuple

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import crud
from api.auth.auth_api import get_current_user
from api.auth.crud import get_user_by_username
from api.main import app
from api.models.task import User


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

        response = await async_client.post(
            f"/users/{user.id}/activities",
            headers={"Authorization": f"Bearer {token}"}
        )
