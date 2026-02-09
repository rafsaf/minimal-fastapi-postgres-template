import logging
import typing

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database_session import new_async_session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/live", response_model=str)
async def live_probe() -> typing.Literal["ok"]:
    return "ok"


@router.get("/health", response_model=str)
async def health_probe(
    _: AsyncSession = Depends(new_async_session),
) -> typing.Literal["app and database ok"]:
    return "app and database ok"
