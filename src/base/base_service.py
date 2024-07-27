from typing import TypeVar, Callable, Awaitable, Generic, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.base import BaseRepository

_T = TypeVar("_T", bound=BaseRepository)
_V = TypeVar("_V")


class BaseService(Generic[_V, _T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _execute(
            self,
            operation: Callable[[AsyncSession], Awaitable[_V | Sequence[_V] | None | bool]]
    ):
        result = await operation(self.session)
        return result

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()

    async def _close(self):
        await self.session.close()
