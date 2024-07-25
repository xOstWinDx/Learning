from typing import TypeVar, Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession

from src.base import BaseRepository

_T = TypeVar("_T", bound=BaseRepository)
_V = TypeVar("_V")


class BaseService:
    def __init__(self, session_factory: Callable[[], Awaitable[AsyncSession]]):
        self.session_factory = session_factory

    async def _execute_transaction(self, operation: Callable[[AsyncSession], Awaitable[_V]]) -> _V:
        session = await self.session_factory()
        try:
            result = await operation(session)
            await session.commit()
            return result
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
