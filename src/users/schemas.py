from pydantic import EmailStr, Field, field_validator

from src.base import BaseSchema
from src.users.utils import hash_password


class UserRead(BaseSchema):
    email: EmailStr
    name: str = Field(max_length=32, min_length=3)


class UserCreate(UserRead):
    hashed_password: str = Field(alias="password")

    @field_validator("hashed_password")
    def hash_pass(cls, v):
        return hash_password(v)


class UserBase(UserCreate):
    ...
