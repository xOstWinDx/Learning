from typing import Any

from pydantic import BaseModel, UUID4, EmailStr, Field


class JwtPayload(BaseModel):
    id: int
    name: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
