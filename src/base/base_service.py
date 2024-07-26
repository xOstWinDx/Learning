from typing import TypeVar, Callable, Awaitable, Generic, Sequence

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.base import BaseRepository

_T = TypeVar("_T", bound=BaseRepository)
_V = TypeVar("_V")


class BaseService(Generic[_V, _T]):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def _execute_transaction(
            self,
            operation: Callable[[AsyncSession], Awaitable[_V | Sequence[_V] | None | bool]]):
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    result = await operation(session)
                    await session.commit()
                    return result
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()

    async def _execute(
            self,
            operation: Callable[[AsyncSession], Awaitable[_V | Sequence[_V] | None | bool]]):
        async with self.session_factory() as session:
            result = await operation(session)
            await session.commit()
        return result
