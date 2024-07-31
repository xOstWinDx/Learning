from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract import AbstractPostgresRepository
from src.abstract.repository import AbstractUserRepository
from src.mixins import DeletePostgresMixin, UpdatePostgresMixin, CreatePostgresMixin, ReadPostgresMixin
from src.models import User


class UserPostgresRepository(
    CreatePostgresMixin[User],
    ReadPostgresMixin[User],
    UpdatePostgresMixin[User],
    DeletePostgresMixin[User],
    AbstractUserRepository,
    AbstractPostgresRepository[User]
):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_one_or_none(self, **filter_by) -> User | None:
        return await self._get_one_or_none(**filter_by)

    async def create_by_entity(self, entity: User) -> User:
        return await self._create_by_entity(entity)

    async def update_by_entity(self, entity: User, **new_data) -> User:
        return await self._update_by_entity(entity, **new_data)

    async def delete_by_entity(self, entity: User) -> None:
        return await self._delete_by_entity(entity)

    async def create_by_data(self, **entity_data) -> User:
        return await self._create_by_data(**entity_data)

    async def get_by_id(self, entity_id: int) -> User:
        return await self._get_one_or_none(id=entity_id)

    async def update_by_id(self, entity_id: int, **new_data) -> User:
        return await self._update_by_id(entity_id, **new_data)

    async def get_all(self, **filter_by) -> Sequence[User]:
        return await self._get_all(**filter_by)

    async def is_exists(self, **filter_by) -> bool:
        query = self.base_exists_query.filter_by(**filter_by)
        return await self.session.scalar(query)

    async def delete_by_id(self, entity_id: int) -> None:
        return await self._delete_by_id(entity_id)
