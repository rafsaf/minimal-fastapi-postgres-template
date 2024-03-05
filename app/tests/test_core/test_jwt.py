import time

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from pydantic import SecretStr

from app.core.config import get_settings
from app.core.security import jwt


def test_jwt_access_token_can_be_decoded_back_into_user_id() -> None:
    user_id = "test_user_id"
    token = jwt.create_jwt_token(user_id)

    payload = jwt.verify_jwt_token(token=token.access_token)
    assert payload.sub == user_id


@freeze_time("2024-01-01")
def test_jwt_payload_is_correct() -> None:
    user_id = "test_user_id"
    token = jwt.create_jwt_token(user_id)

    assert token.payload.iat == int(time.time())
    assert token.payload.sub == user_id
    assert token.payload.iss == get_settings().security.jwt_issuer
    assert (
        token.payload.exp
        == int(time.time()) + get_settings().security.jwt_access_token_expire_secs
    )


def test_jwt_error_after_exp_time() -> None:
    user_id = "test_user_id"
    with freeze_time("2024-01-01"):
        token = jwt.create_jwt_token(user_id)
    with freeze_time("2024-02-01"):
        with pytest.raises(HTTPException) as e:
            jwt.verify_jwt_token(token=token.access_token)

        assert e.value.detail == "Token invalid: Signature has expired"


def test_jwt_error_before_iat_time() -> None:
    user_id = "test_user_id"
    with freeze_time("2024-01-01"):
        token = jwt.create_jwt_token(user_id)
    with freeze_time("2023-12-01"):
        with pytest.raises(HTTPException) as e:
            jwt.verify_jwt_token(token=token.access_token)

        assert e.value.detail == "Token invalid: The token is not yet valid (iat)"


def test_jwt_error_with_invalid_token() -> None:
    with pytest.raises(HTTPException) as e:
        jwt.verify_jwt_token(token="invalid!")

    assert e.value.detail == "Token invalid: Not enough segments"


def test_jwt_error_with_invalid_issuer() -> None:
    user_id = "test_user_id"
    token = jwt.create_jwt_token(user_id)

    get_settings().security.jwt_issuer = "another_issuer"

    with pytest.raises(HTTPException) as e:
        jwt.verify_jwt_token(token=token.access_token)

    assert e.value.detail == "Token invalid: Invalid issuer"


def test_jwt_error_with_invalid_secret_key() -> None:
    user_id = "test_user_id"
    token = jwt.create_jwt_token(user_id)

    get_settings().security.jwt_secret_key = SecretStr("the secret has changed now!")

    with pytest.raises(HTTPException) as e:
        jwt.verify_jwt_token(token=token.access_token)

    assert e.value.detail == "Token invalid: Signature verification failed"
