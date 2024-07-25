import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import BIGINT, String, JSON, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from src.config import CONFIG

engine = create_async_engine(
    url=CONFIG.database_url,
    echo=CONFIG.DEBUG_MODE,
    pool_size=10,
    max_overflow=100
)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

bigint = Annotated[int, int]
str2 = Annotated[str, 2]
str8 = Annotated[str, 8]
str16 = Annotated[str, 16]
str32 = Annotated[str, 32]
id_ = Annotated[UUID, mapped_column(primary_key=True, unique=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.current_timestamp())]


class BaseModel(DeclarativeBase):
    type_annotation_map = {
        bigint: BIGINT,
        str2: String(2),
        str8: String(8),
        str16: String(16),
        str32: String(32),
        dict: JSON
    }
    id: Mapped[id_]
    created_at: Mapped[created_at]

from .users.models import User  # noqa
