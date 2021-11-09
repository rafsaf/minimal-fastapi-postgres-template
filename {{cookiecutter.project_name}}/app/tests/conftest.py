import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Base
from app.session import async_engine, async_session
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
async def test_db_setup_sessionmaker():
    assert settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == settings.TEST_SQLALCHEMY_DATABASE_URI

    async with async_engine.begin() as conn:
        # awalys drop and create test db tables between tests session
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        yield session
