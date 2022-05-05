from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    id: str
    email: EmailStr
    full_name: str | None


class UserUpdate(BaseUser):
    email: EmailStr | None
    password: str | None
    full_name: str | None


class UserCreate(BaseUser):
    email: EmailStr
    password: str
    full_name: str
