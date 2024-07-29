import bcrypt
from pydantic import BaseModel, EmailStr, Field

from src.base import BaseSchema


class UserBase(BaseModel):
    email: EmailStr | None
    name: str = Field(max_length=32, min_length=3)


class UserCreate(UserBase):
    password: str | None = Field(default=None, min_length=8)


class UserResponse(BaseSchema, UserBase):
    is_admin: bool


class UserAll(UserResponse):
    hashed_password: bytes | None = None

    def check_password(self, plain_password: str) -> bool:
        if self.hashed_password is None:
            return False
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password)


class JwtPayload(BaseModel):
    id: int
    name: str
