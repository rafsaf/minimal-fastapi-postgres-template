import time

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.core.config import get_settings

JWT_ALGORITHM = "HS256"


# Payload follows RFC 7519
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
    # Pay attention to verify_signature passed explicite, even if it is the default.
    # Verification is based on expected payload fields like "exp", "iat" etc.
    # so if you rename for example "exp" to "my_custom_exp", this is gonna break,
    # jwt.ExpiredSignatureError will not be raised, that can potentialy
    # be major security risk - not validating tokens at all.
    # If unsure, jump into jwt.decode code, make sure tests are passing
    # https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256

    try:
        raw_payload = jwt.decode(
            token,
            get_settings().security.jwt_secret_key.get_secret_value(),
            algorithms=[JWT_ALGORITHM],
            options={"verify_signature": True},
            issuer=get_settings().security.jwt_issuer,
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid: {e}",
        )

    return JWTTokenPayload(**raw_payload)
