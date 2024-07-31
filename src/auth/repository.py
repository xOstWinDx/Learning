from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.repository import AbstractAuthRepository
from src.mixins import ReadPostgresMixin, CreatePostgresMixin
from src.models import User


class AuthPostgresRepository(CreatePostgresMixin, ReadPostgresMixin, AbstractAuthRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def create_by_data(self, **entity_data) -> User:
        return await self._create_by_data(**entity_data)

    async def is_exists(self, **filter_by) -> bool:
        return await self.session.scalar(
            select(exists(User)).
            filter_by(**filter_by)
        )

    async def get_one_or_none(self, **filter_by) -> User:
        return await self._get_one_or_none(**filter_by)
