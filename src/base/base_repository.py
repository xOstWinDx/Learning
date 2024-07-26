from typing import TypeVar, Generic, Type, Sequence

from sqlalchemy import Executable, select, exists, insert, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseModel

_T = TypeVar('_T', bound=BaseModel)


class BaseRepository(Generic[_T]):

    def __init__(self, model: Type[_T], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, **data) -> None:
        stmt = (
            insert(self.model).
            values(**data)
        )
        await self._execute(stmt)

    async def get_one_or_none(self, **filter_by) -> _T:
        query = (
            select(self.model).
            filter_by(**filter_by)
        )
        res = await self._execute(query)
        return res.scalar_one_or_none()

    async def get_all(self, **filter_by) -> Sequence[_T]:
        query = (
            select(self.model).
            filter_by(**filter_by)
        )
        res = await self._execute(query)
        return res.scalars().all()

    async def is_exists(self, **filter_by) -> bool:
        query = (
            select(exists(self.model))
            .filter_by(**filter_by)
        )
        res = await self._execute(query)
        return res.scalar()

    async def _execute(self, stmt: Executable) -> Result:
        return await self.session.execute(stmt)

    async def delete(self, model: _T) -> None:
        await self.session.delete(model)
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
