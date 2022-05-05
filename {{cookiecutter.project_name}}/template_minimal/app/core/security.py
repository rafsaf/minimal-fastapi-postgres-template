"""Black-box security shortcuts to generate JWT tokens and password hashing and verifcation."""

from datetime import datetime

import jwt
from passlib.context import CryptContext

from app.core import config

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECS = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_TOKEN_EXPIRE_SECS = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=config.settings.SECURITY_BCRYPT_DEFAULT_ROUNDS,
)


def create_jwt_token(subject: str | int, exp_secs: int, refresh: bool):
    """Creates jwt access or refresh token for user."""

    iat = datetime.utcnow().timestamp()
    exp = iat + exp_secs

    to_encode = {
        "iat": iat,
        "exp": exp,
        "sub": str(subject),
        "refresh": refresh,
    }
    encoded_jwt: str = jwt.encode(
        to_encode,
        key=config.settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return encoded_jwt, exp, iat


def access_token_response(subject: str | int):
    access_token, exp, iat = create_jwt_token(
        subject, ACCESS_TOKEN_EXPIRE_SECS, refresh=False
    )
    refresh_token, refresh_exp, refresh_iat = create_jwt_token(
        subject, REFRESH_TOKEN_EXPIRE_SECS, refresh=True
    )
    return {
        "token_type": "Bearer",
        "access_token": access_token,
        "expires_at": exp,
        "issued_at": iat,
        "refresh_token": refresh_token,
        "refresh_token_expires_at": refresh_exp,
        "refresh_token_issued_at": refresh_iat,
    }


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
