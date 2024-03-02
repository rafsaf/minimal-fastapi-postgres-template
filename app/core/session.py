"""
SQLAlchemy async engine and sessions tools

https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings

async_engine = create_async_engine(
    get_settings().sqlalchemy_database_uri, pool_pre_ping=True
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
