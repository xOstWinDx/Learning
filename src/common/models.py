import bcrypt
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel, str16, str32


class User(BaseModel):
    __tablename__ = "user"

    hashed_password: Mapped[bytes | None]
    email: Mapped[str32 | None] = mapped_column(index=True, unique=True)
    telegram_id: Mapped[int | None] = mapped_column(unique=True)
    name: Mapped[str16] = mapped_column(index=True)
    is_admin: Mapped[bool]

    def check_password(self, plain_password: str) -> bool:
        if self.hashed_password is None:
            return False
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password)
