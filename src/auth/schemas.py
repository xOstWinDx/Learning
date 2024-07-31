from pydantic import BaseModel, EmailStr, Field

from src.schemas import UserBase


class UserCreate(UserBase):
    password: str | None = Field(default=None, min_length=8)


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class JwtPayload(BaseModel):
    id: int
    name: str
