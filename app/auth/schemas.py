from pydantic import BaseModel, ConfigDict, EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserUpdatePasswordRequest(BaseModel):
    password: str


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class AccessTokenResponse(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    user_id: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
