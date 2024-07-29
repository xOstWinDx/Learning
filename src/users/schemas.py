from pydantic import EmailStr, Field, BaseModel

from src.base import BaseSchema


class UserBase(BaseModel):
    email: EmailStr | None
    name: str = Field(max_length=32, min_length=3)


class UserCreate(UserBase):
    id: int


class UserResponse(BaseSchema, UserBase):
    is_admin: bool


class UserAll(UserResponse):
    ...
