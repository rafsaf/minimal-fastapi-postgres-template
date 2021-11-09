import asyncio
from typing import AsyncGenerator, Optional

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash
from app.main import app
from app.models import Base, User
from app.session import async_engine, async_session


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
    # assert if we use TEST_DB URL for 100%
    assert settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        yield session


@pytest.fixture
async def default_user(session: AsyncSession):
    result = await session.execute(select(User).where(User.email == "user@email.com"))
    user: Optional[User] = result.scalars().first()
    if user is None:
        new_user = User(
            email="user@email.com",
            hashed_password=get_password_hash("password"),
            full_name="fullname",
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    return user
