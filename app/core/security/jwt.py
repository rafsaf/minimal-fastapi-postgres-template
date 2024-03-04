import time

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.api import api_messages
from app.core.config import get_settings

JWT_ALGORITHM = "HS256"


# https://www.rfc-editor.org/rfc/rfc7519#section-4.1
class JWTTokenPayload(BaseModel):
    iss: str
    sub: str
    exp: int
    iat: int


class JWTToken(BaseModel):
    payload: JWTTokenPayload
    access_token: str


def create_jwt_token(user_id: str) -> JWTToken:
    iat = int(time.time())
    exp = iat + get_settings().security.jwt_access_token_expire_secs

    token_payload = JWTTokenPayload(
        iss=get_settings().security.jwt_issuer,
        sub=user_id,
        exp=exp,
        iat=iat,
    )

    access_token = jwt.encode(
        token_payload.model_dump(),
        key=get_settings().security.jwt_secret_key.get_secret_value(),
        algorithm=JWT_ALGORITHM,
    )

    return JWTToken(payload=token_payload, access_token=access_token)


def verify_jwt_token(token: str) -> JWTTokenPayload:
    try:
        raw_payload = jwt.decode(
            token,
            get_settings().security.jwt_secret_key.get_secret_value(),
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=api_messages.JWT_ERROR_EXPIRED_TOKEN,
        )
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=api_messages.JWT_ERROR_INVALID_TOKEN,
        )

    return JWTTokenPayload(**raw_payload)
