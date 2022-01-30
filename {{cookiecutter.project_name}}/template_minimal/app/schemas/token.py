from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    expire_at: datetime
    refresh_token: str
    refresh_expire_at: datetime


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    refresh: Optional[bool] = None


class TokenRefresh(BaseModel):
    refresh_token: str
