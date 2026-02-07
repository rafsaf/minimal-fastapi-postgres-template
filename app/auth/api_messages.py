from typing import Any

JWT_ERROR_USER_REMOVED = "User removed"
PASSWORD_INVALID = "Incorrect email or password"
REFRESH_TOKEN_NOT_FOUND = "Refresh token not found"
REFRESH_TOKEN_EXPIRED = "Refresh token expired"
REFRESH_TOKEN_ALREADY_USED = "Refresh token already used"
EMAIL_ADDRESS_ALREADY_USED = "Cannot use this email address"


UNAUTHORIZED_RESPONSES: dict[int | str, dict[str, Any]] = {
    401: {
        "description": "No `Authorization` access token header, token is invalid or user removed",
        "content": {
            "application/json": {
                "examples": {
                    "not authenticated": {
                        "summary": "No authorization token header",
                        "value": {"detail": "Not authenticated"},
                    },
                    "invalid token": {
                        "summary": "Token validation failed, decode failed, it may be expired or malformed",
                        "value": {"detail": "Token invalid: {detailed error msg}"},
                    },
                    "removed user": {
                        "summary": JWT_ERROR_USER_REMOVED,
                        "value": {"detail": JWT_ERROR_USER_REMOVED},
                    },
                }
            }
        },
    }
}

ACCESS_TOKEN_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Invalid email or password",
        "content": {"application/json": {"example": {"detail": PASSWORD_INVALID}}},
    },
}

REFRESH_TOKEN_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Refresh token expired or is already used",
        "content": {
            "application/json": {
                "examples": {
                    "refresh token expired": {
                        "summary": REFRESH_TOKEN_EXPIRED,
                        "value": {"detail": REFRESH_TOKEN_EXPIRED},
                    },
                    "refresh token already used": {
                        "summary": REFRESH_TOKEN_ALREADY_USED,
                        "value": {"detail": REFRESH_TOKEN_ALREADY_USED},
                    },
                }
            }
        },
    },
    404: {
        "description": "Refresh token does not exist",
        "content": {
            "application/json": {"example": {"detail": REFRESH_TOKEN_NOT_FOUND}}
        },
    },
}
