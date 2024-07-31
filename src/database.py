import datetime
from typing import Annotated, AsyncGenerator

from sqlalchemy import BIGINT, String, JSON, func, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from src.config import CONFIG

if CONFIG.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
    engine = create_async_engine(
        url=CONFIG.test_database_url, echo=False, **DATABASE_PARAMS
    )
else:
    engine = create_async_engine(url=CONFIG.database_url, echo=False)

session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


bigint = Annotated[int, int]
str2 = Annotated[str, 2]
str8 = Annotated[str, 8]
str16 = Annotated[str, 16]
str32 = Annotated[str, 32]
id_ = Annotated[int, mapped_column(primary_key=True, unique=True, index=True, autoincrement=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.current_timestamp())]


class BaseModel(DeclarativeBase):
    type_annotation_map = {
        bigint: BIGINT,
        str2: String(2),
        str8: String(8),
        str16: String(16),
        str32: String(32),
        id_: BIGINT,
        dict: JSON
    }
    id: Mapped[id_]
    created_at: Mapped[created_at]
