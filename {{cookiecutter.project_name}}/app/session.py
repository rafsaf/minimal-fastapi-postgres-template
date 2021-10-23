from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import sessionmaker


from app.core.config import settings

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

AsyncSessionLocal = AsyncSession(async_engine, expire_on_commit=False)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
