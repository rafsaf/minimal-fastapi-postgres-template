# SQLAlchemy async engine and sessions tools
#
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
#
# for pool size configuration:
# https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool


from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


def new_async_engine(uri: URL) -> AsyncEngine:
    return create_async_engine(
        uri,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30.0,
        pool_recycle=600,
    )


_ASYNC_ENGINE = new_async_engine(get_settings().sqlalchemy_database_uri)
_ASYNC_SESSIONMAKER = async_sessionmaker(_ASYNC_ENGINE, expire_on_commit=False)


async def new_async_session() -> AsyncGenerator[AsyncSession]:
    session = _ASYNC_SESSIONMAKER()
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def new_script_async_session() -> AsyncGenerator[AsyncSession]:
    _engine = create_async_engine(
        get_settings().sqlalchemy_database_uri, pool_pre_ping=True
    )
    _async_sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)

    session = _async_sessionmaker()
    try:
        yield session
    finally:
        await session.close()
        await _engine.dispose()
