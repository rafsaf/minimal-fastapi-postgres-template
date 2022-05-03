"""Black-box security shortcuts to generate JWT tokens and password hashing and verifcation."""

from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.core import config

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=config.settings.SECURITY_BCRYPT_DEFAULT_ROUNDS,
)


ALGORITHM = "HS256"


def create_access_token(subject: str | int) -> tuple[str, datetime]:
    """Creates jwt access token for user.

    Returns tuple with generated token and expire datetime.
    expire minutes may be set using ACCESS_TOKEN_EXPIRE_MINUTES.

    Args:
        subject: anything unique to user, eg. id, email.
    """

    now = datetime.utcnow()
    expire = now + timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": False}
    encoded_jwt: str = jwt.encode(
        to_encode,
        key=config.settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt, expire


def create_refresh_token(subject: str | int) -> tuple[str, datetime]:
    """Creates jwt refresh token for user.

    Returns tuple with generated token and expire datetime.
    expire minutes may be set using REFRESH_TOKEN_EXPIRE_MINUTES.

    Args:
        subject: anything unique to user, eg. id, email.
    """

    now = datetime.utcnow()
    expire = now + timedelta(minutes=config.settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": True}
    encoded_jwt: str = jwt.encode(
        to_encode,
        key=config.settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt, expire


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifie plain and hashed password matches

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Create hash from password

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return pwd_context.hash(password)
