from fastapi import APIRouter

from app.api import api_messages
from app.api.endpoints import auth, users

auth_router = APIRouter()
auth_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router = APIRouter(
    responses={
        401: {
            "description": "No `Authorization` access token header or token is invalid",
            "content": {
                "application/json": {
                    "examples": {
                        "not authenticated": {
                            "summary": "No authorization token header",
                            "value": {"detail": "Not authenticated"},
                        },
                        "invalid token": {
                            "summary": api_messages.JWT_ERROR_INVALID_TOKEN,
                            "value": {"detail": api_messages.JWT_ERROR_INVALID_TOKEN},
                        },
                    }
                }
            },
        },
        403: {
            "description": "Access token is expired or user was removed",
            "content": {
                "application/json": {
                    "examples": {
                        "expired token": {
                            "summary": api_messages.JWT_ERROR_EXPIRED_TOKEN,
                            "value": {"detail": api_messages.JWT_ERROR_EXPIRED_TOKEN},
                        },
                        "removed user": {
                            "summary": api_messages.JWT_ERROR_USER_REMOVED,
                            "value": {"detail": api_messages.JWT_ERROR_USER_REMOVED},
                        },
                    },
                }
            },
        },
    }
)
api_router.include_router(users.router, prefix="/users", tags=["users"])