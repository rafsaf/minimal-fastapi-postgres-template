import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import prometheus_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.auth.views import router as auth_router
from app.core import database_session, metrics
from app.core.config import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    logger.info("starting application...")
    if get_settings().prometheus.enabled:
        logger.info(
            "starting prometheus client server on interface %s port %d",
            get_settings().prometheus.addr,
            get_settings().prometheus.port,
        )

        prometheus_client.start_http_server(
            addr=get_settings().prometheus.addr,
            port=get_settings().prometheus.port,
        )
        metrics.APP_STARTED.inc()

    yield

    logger.info("shutting down application...")

    await database_session._ASYNC_ENGINE.dispose()
    logger.info("disposed database engine and closed connections...")

    if get_settings().prometheus.enabled:
        logger.info(
            "stopping prometheus with delay of %d seconds...",
            get_settings().prometheus.stop_delay_secs,
        )
        metrics.APP_STOPPED.inc()
        await asyncio.sleep(get_settings().prometheus.stop_delay_secs)

    logger.info("bye! application shutdown completed")


app = FastAPI(
    title="minimal fastapi postgres template",
    version="7.0.0",
    description="https://github.com/rafsaf/minimal-fastapi-postgres-template",
    openapi_url="/openapi.json",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().security.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guards against HTTP Host Header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=get_settings().security.allowed_hosts,
)
