# SQLAlchemy async engine and sessions tools
#
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
#
# for pool size configuration:
# https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings

ASYNC_ENGINE = create_async_engine(
    get_settings().sqlalchemy_database_uri,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30.0,
    pool_recycle=600,
)
ASYNC_SESSIONMAKER = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)
