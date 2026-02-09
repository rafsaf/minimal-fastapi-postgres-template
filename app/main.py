import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.auth.views import router as auth_router
from app.core import lifespan
from app.core.config import get_settings
from app.probe.views import router as probe_router

logger = logging.getLogger(__name__)


app = FastAPI(
    title="minimal fastapi postgres template",
    version="7.0.0",
    description="https://github.com/rafsaf/minimal-fastapi-postgres-template",
    openapi_url="/openapi.json",
    docs_url="/",
    lifespan=lifespan.lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(probe_router, prefix="/probe", tags=["probe"])

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
