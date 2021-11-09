from pathlib import Path
from typing import Dict, List, Literal, Union

import toml
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator

PROJECT_DIR = Path(__file__).parent.parent.parent
pyproject_content = toml.load(f"{PROJECT_DIR}/pyproject.toml")["tool"]["poetry"]


class Settings(BaseSettings):
    # CORE SETTINGS
    SECRET_KEY: str
    ENVIRONMENT: Literal["DEV", "PYTEST", "STAGE", "PRODUCTION"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]]

    # PROJECT NAME, API PREFIX, VERSION AND DESC, CORS ORIGINS
    PROJECT_NAME: str = pyproject_content["name"]
    VERSION: str = pyproject_content["version"]
    DESCRIPTION: str = pyproject_content["description"]

    # POSTGRESQL DEFAULT DATABASE
    DEFAULT_DATABASE_HOSTNAME: str
    DEFAULT_DATABASE_USER: str
    DEFAULT_DATABASE_PASSWORD: str
    DEFAULT_DATABASE_PORT: str
    DEFAULT_DATABASE_DB: str
    DEFAULT_SQLALCHEMY_DATABASE_URI: str = ""

    # POSTGRESQL TEST DATABASE
    TEST_DATABASE_HOSTNAME: str
    TEST_DATABASE_USER: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_PORT: str
    TEST_DATABASE_DB: str
    TEST_SQLALCHEMY_DATABASE_URI: str = ""

    # FIRST SUPERUSER
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS")
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("DEFAULT_SQLALCHEMY_DATABASE_URI")
    def _assemble_default_db_connection(cls, v: str, values: Dict[str, str]) -> str:
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values["DEFAULT_DATABASE_USER"],
            password=values["DEFAULT_DATABASE_PASSWORD"],
            host=values["DEFAULT_DATABASE_HOSTNAME"],
            port=values["DEFAULT_DATABASE_PORT"],
            path=f"/{values['DEFAULT_DATABASE_DB']}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI")
    def _assemble_test_db_connection(cls, v: str, values: Dict[str, str]) -> str:
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values["TEST_DATABASE_USER"],
            password=values["TEST_DATABASE_PASSWORD"],
            host=values["TEST_DATABASE_HOSTNAME"],
            port=values["TEST_DATABASE_PORT"],
            path=f"/{values['TEST_DATABASE_DB']}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings: Settings = Settings()
