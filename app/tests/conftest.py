import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.core import database_session
from app.core.security.jwt import create_jwt_token
from app.core.security.password import get_password_hash
from app.main import app as fastapi_app
from app.models import Base, User

default_user_id = "b75365d9-7bf9-4f54-add5-aeab333a087b"
default_user_email = "geralt@wiedzmin.pl"
default_user_password = "geralt"
default_user_password_hash = get_password_hash(default_user_password)
default_user_access_token = create_jwt_token(default_user_id)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def fixture_db_setup_tables_and_start_broad_connection() -> None:
    # always drop and create test db tables between tests session
    async with database_session.ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def fixture_mock_async_session_factory(
    fixture_db_setup_tables_and_start_broad_connection: None,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[None, None]:
    # we want to monkeypatch sessionmaker with one bound to session
    # that we will rollback on function scope
    async with database_session.ASYNC_ENGINE.connect() as conn:
        async with conn.begin() as transaction:
            session = AsyncSession(bind=conn, expire_on_commit=False)

            # trick sessionmaker instance to use our crafted session
            # that will have rollback on the end of each test
            # note, magic methods goes directly to class __call__ definition
            # so we need ugly hack with class overwrite
            # maybe it can be done better
            class mock_async_sessionmaker(async_sessionmaker):
                def __call__(self, **local_kw: Any) -> Any:
                    return session

            session_factory_mock = mock_async_sessionmaker(
                bind=database_session.ASYNC_ENGINE, expire_on_commit=False
            )
            monkeypatch.setattr(
                database_session,
                "ASYNC_SESSIONMAKER",
                session_factory_mock,
            )

            yield

            await session.close()
            await transaction.rollback()


@pytest_asyncio.fixture(name="session")
async def fixture_session(
    fixture_mock_async_session_factory: None,
) -> AsyncGenerator[AsyncSession, None]:
    async with database_session.ASYNC_SESSIONMAKER() as session:
        yield session


@pytest_asyncio.fixture(name="client")
async def fixture_client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture(name="default_user")
async def fixture_default_user(session: AsyncSession) -> User:
    default_user = User(
        user_id=default_user_id,
        email=default_user_email,
        hashed_password=default_user_password_hash,
    )
    session.add(default_user)
    await session.commit()
    await session.refresh(default_user)
    return default_user


@pytest.fixture(name="default_user_headers")
def fixture_default_user_headers(default_user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {default_user_access_token}"}
