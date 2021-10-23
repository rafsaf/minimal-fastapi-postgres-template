from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
