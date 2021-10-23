from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # DEBUG
    DEBUG: bool
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # SECURITY
    SECRET_KEY: str

    # PROJECT NAME, API PREFIX, VERSION AND DESC, CORS ORIGINS
    PROJECT_NAME: str
    API_STR: str
    VERSION: str
    DESCRIPTION: str
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]]

    # POSTGRESQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str = ""

    # FIRST SUPERUSER
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # VALIDATORS

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def _assemble_db_connection(cls, v: str, values: Dict[str, Optional[str]]) -> str:
        if v != "":
            return v
        if values.get("DEBUG"):
            postgres_server = "localhost"
        else:
            assert (
                values.get("POSTGRES_SERVER") is not None
            ), "Variable POSTGRES_SERVER cannot be None"

            postgres_server = values.get("POSTGRES_SERVER")

        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=postgres_server or "localhost",
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings: Settings = Settings()
