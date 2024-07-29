from sqlalchemy.orm import Mapped, mapped_column

from src.database import str32, str16, BaseModel


class User(BaseModel):
    __tablename__ = "user"

    email: Mapped[str32 | None] = mapped_column(unique=True, index=True)
    name: Mapped[str16] = mapped_column(index=True)
    is_admin: Mapped[bool]
