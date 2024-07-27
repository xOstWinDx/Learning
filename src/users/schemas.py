from pydantic import EmailStr, Field, BaseModel

from src.base import BaseSchema


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(max_length=32, min_length=3)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserResponse(BaseSchema, UserBase):
    is_admin: bool


class UserAll(UserResponse):
    hashed_password: bytes



