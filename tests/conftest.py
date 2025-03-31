from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import close_all_sessions

from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/test-demo?charset=utf8"

@pytest_asyncio.fixture(scope="function")
async def test_async_generator() -> AsyncGenerator[AsyncClient, AsyncSession]:
    async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
    async_session = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_session()
    
    async def get_db_for_testing():
        yield session

    app.dependency_overrides[get_db] = get_db_for_testing

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client, session  # クライアントとセッションの両方を返す
        
    await session.close()
