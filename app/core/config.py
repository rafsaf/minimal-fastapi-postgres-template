# File with environment variables and general configuration logic.
# Env variables are combined in nested groups like "Security", "Database" etc.
# So environment variable (case-insensitive) for jwt_secret_key will be "security__jwt_secret_key"
#
# Pydantic priority ordering:
#
# 1. (Most important, will overwrite everything) - environment variables
# 2. `.env` file in root folder of project
# 3. Default values
#
# "sqlalchemy_database_uri" is computed field that will create valid database URL
#
# See https://pydantic-docs.helpmanual.io/usage/settings/
# Note, complex types like lists are read as json-encoded strings.


import logging.config
from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent


class Security(BaseModel):
    jwt_issuer: str = "my-app"
    jwt_secret_key: SecretStr = SecretStr(
        "change-me-to-a-strong-secret-key-at-least-32-chars-long"
    )
    jwt_access_token_expire_secs: int = Field(default=15 * 60, gt=10)  # 15min
    jwt_refresh_token_expire_secs: int = Field(default=28 * 24 * 3600, gt=60)  # 28d
    jwt_algorithm: str = "HS256"

    password_bcrypt_rounds: int = 12
    allowed_hosts: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    backend_cors_origins: list[AnyHttpUrl] = []


class Database(BaseModel):
    hostname: str = "postgres"
    username: str = "postgres"
    password: SecretStr = SecretStr("passwd-change-me")
    port: int = 5432
    db: str = "postgres"


class Prometheus(BaseModel):
    enabled: bool = False
    port: int = 9090
    addr: str = "127.0.0.1"
    stop_delay_secs: int = 0


class Settings(BaseSettings):
    security: Security = Field(default_factory=Security)
    database: Database = Field(default_factory=Database)
    prometheus: Prometheus = Field(default_factory=Prometheus)

    log_level: str = "INFO"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.database.username,
            password=self.database.password.get_secret_value(),
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.db,
        )

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def logging_config(log_level: str) -> None:
    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} [{levelname}] {name}: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "": {
                "level": log_level,
                "handlers": ["stream"],
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(conf)


logging_config(log_level=get_settings().log_level)
