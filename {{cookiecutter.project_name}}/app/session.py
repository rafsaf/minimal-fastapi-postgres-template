from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

if settings.ENVIRONMENT == "PYTEST":
    SQLALCHEMY_DATABASE_URI = settings.TEST_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = settings.DEFAULT_SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
