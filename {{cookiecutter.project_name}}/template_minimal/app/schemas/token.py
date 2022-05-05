from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class TokenPayload(BaseModel):
    sub: str | None = None
    refresh: bool | None = None
    iat: float
    exp: float


class TokenRefresh(BaseModel):
    refresh_token: str
