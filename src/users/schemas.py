import bcrypt

from src.schemas import BaseSchema, UserBase


class UserResponse(BaseSchema, UserBase):
    is_admin: bool


class UserAll(UserResponse):
    telegram_id: int | None = None
    hashed_password: bytes | None = None

    def check_password(self, plain_password: str) -> bool:
        if self.hashed_password is None:
            return False
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password)
