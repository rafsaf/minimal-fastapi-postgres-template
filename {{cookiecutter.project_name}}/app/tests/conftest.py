from os import environ, getenv

# We overwrite variables from .env to hardcoded ones to connect with tests database
# Note, order matters!
# If we write `from app.main import app` BEFORE hardcoding environment,
# It would use postgres settings defined in .env file instead of those below.

environ["POSTGRES_USER"] = "tests"
environ["POSTGRES_PASSWORD"] = "tests"
environ["POSTGRES_DB"] = "tests"
environ["POSTGRES_HOST"] = getenv("TESTS_POSTGRES_DB_HOST") or "localhost"
environ["POSTGRES_PORT"] = "37645"

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings
from app.main import app
from app.models import Base


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
    async_test_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    async with async_test_engine.begin() as conn:
        # awalys drop and create test db tables between tests session
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_test_session = sessionmaker(
        async_test_engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_test_session


@pytest.fixture
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        yield session
