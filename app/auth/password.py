import bcrypt

from app.core.config import get_settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(get_settings().security.password_bcrypt_rounds),
    ).decode()


DUMMY_PASSWORD = get_password_hash("")
