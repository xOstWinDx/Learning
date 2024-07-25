from typing import TypeVar, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseModel

_T = TypeVar('_T', bound=BaseModel)


class BaseRepository:
    model: _T = BaseModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: _T) -> None:
        self.session.add(model)
        await self.session.flush()

    async def get(self, ident: Any | tuple[Any, ...]) -> _T:
        return await self.session.get(self.model, ident)

    async def delete(self, model: _T) -> None:
        await self.session.delete(model)
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
