from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

if settings.ENVIRONMENT == "PYTEST":
    sqlalchemy_database_uri = settings.TEST_SQLALCHEMY_DATABASE_URI
else:
    sqlalchemy_database_uri = settings.DEFAULT_SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
