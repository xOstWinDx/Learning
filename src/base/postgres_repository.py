from typing import Sequence, TypeVar, Type

from sqlalchemy import select,update, exists, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract import AbstractPostgresRepository
from src.database import BaseModel

T = TypeVar('T', bound=BaseModel)


class BasePostgresRepository(AbstractPostgresRepository[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        super().__init__(session=session, model=model)

    async def create_by_entity(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def update_by_entity(self, entity: T, **new_data) -> T:
        for key, value in new_data.items():
            setattr(entity, key, value)
        await self.session.flush()
        return entity

    async def delete_by_entity(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()

    async def create_by_data(self, **entity_data) -> int:
        res = await self.session.execute(
            insert(self.model).
            values(**entity_data).
            returning(self.model.id)
        )
        return res.scalar()

    async def get_by_id(self, entity_id: int) -> T:
        return await self.session.get(self.model, entity_id)

    async def get_one_or_none(self, **filter_by) -> T | None:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.one_or_none()

    async def update_by_id(self, entity_id: int, **new_data) -> None:
        await self.session.execute(
            update(self.model).
            where(self.model.id == entity_id).
            values(**new_data)
        )
        await self.session.flush()

    async def get_all(self, **filter_by) -> Sequence[T]:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.all()

    async def is_exists(self, **filter_by) -> bool:
        return await self.session.scalar(
            select(exists(self.model)).
            filter_by(**filter_by)
        )

    async def delete_by_id(self, entity_id: int) -> None:
        await self.session.execute(
            delete(self.model).
            where(self.model.id == entity_id)
        )
        await self.session.flush()
