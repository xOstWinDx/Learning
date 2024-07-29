from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.repository import AbstractPostgresRepository
from src.users.models import User


class UserRepository(AbstractPostgresRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_one_or_none(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None,

    ) -> User:
        query = self._query_filters_builder(
            self.base_select_query,
            id=id,
            email=email,
            name=name,
            is_admin=is_admin
        )
        res = await self._execute(query)
        return res.scalar_one_or_none()

    async def get_all(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None,
    ) -> Sequence[User]:
        query = self._query_filters_builder(
            self.base_select_query,
            id=id,
            email=email,
            name=name,
            is_admin=is_admin
        )

        res = await self._execute(query)
        return res.scalars().all()

    async def is_exists(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None,
    ) -> bool:
        query = self._query_filters_builder(
            self.base_exists_query,
            id=id,
            email=email,
            name=name,
            is_admin=is_admin
        )
        res = await self._execute(query)
        return res.scalar()

    async def delete(self, user_id: int) -> None:
        query = self.base_delete_stmt.where(self.model.id == user_id)
        await self._execute(query)

    async def add(
            self,
            id: int,  # noqa
            email: str | None,
            name: str,
            is_admin: bool = False
    ) -> User:
        query = (
            self.base_insert_stmt.
            values(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            ).
            returning(self.model)
        )
        res = await self._execute(query)
        return res.scalar_one()

    async def update(self, id: int, **entity_data) -> User:  # noqa
        query = (
            self.base_update_stmt.
            where(self.model.id == id).
            values(**entity_data).
            returning(self.model)
        )
        res = await self._execute(query)
        return res.scalar_one()



