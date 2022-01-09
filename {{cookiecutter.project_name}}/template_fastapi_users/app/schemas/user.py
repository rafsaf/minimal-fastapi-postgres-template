from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    email: EmailStr
    full_name: str


class UserUpdate(BaseUser):
    email: Optional[EmailStr]
    password: Optional[str]
    full_name: Optional[str]


class UserCreate(BaseUser):
    email: EmailStr
    password: str
    full_name: str
