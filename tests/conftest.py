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
async def db():
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
    async_session = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にテーブルを初期化
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更、テスト関数内で使うDBセッションと共用させる
    shared_session = async_session()
    async def get_test_db():
        yield shared_session

    app.dependency_overrides[get_db] = get_test_db
    yield shared_session  # テスト関数にDBセッションを渡す（これは実環境と共用）

    await shared_session.rollback()  # テスト後にロールバック
    close_all_sessions()  # テスト後にセッションを閉じる
    await async_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c
