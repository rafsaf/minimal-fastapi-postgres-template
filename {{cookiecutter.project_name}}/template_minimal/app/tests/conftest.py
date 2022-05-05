import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, security
from app.main import app
from app.models import Base, User
from app.session import async_engine, async_session

default_user_email = "geralt@wiedzmin.pl"
default_user_password = "geralt"
default_user_hash = security.get_password_hash(default_user_password)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == config.settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        session: AsyncSession

        yield session

        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture()
async def default_user(session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.email == default_user_email))
    user: User | None = result.scalars().first()
    if user is None:
        new_user = User(
            email=default_user_email,
            hashed_password=default_user_hash,
            full_name="fullname",
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    return user


@pytest_asyncio.fixture()
async def default_user_headers(client: AsyncClient, default_user: User):
    access_token = await client.post(
        app.url_path_for("access_token"),
        data={
            "username": default_user_email,
            "password": default_user_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return {"Authorization": f"Bearer {access_token.json()['access_token']}"}
