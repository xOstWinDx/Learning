from typing import TypeVar, Type, Generic, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseModel

T = TypeVar('T', bound=BaseModel)


class BasePostgresMixin(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model


class CreatePostgresMixin(BasePostgresMixin[T]):
    async def _create_by_data(self, **entity_data) -> T:
        entity = self.model(**entity_data)
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def _create_by_entity(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity


class ReadPostgresMixin(BasePostgresMixin[T]):
    async def _get_one_or_none(self, **filter_by) -> T | None:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.one_or_none()

    async def _get_all(self, **filter_by) -> Sequence[T]:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.all()


class UpdatePostgresMixin(BasePostgresMixin[T]):
    async def _update_by_id(self, entity_id: int, **new_data) -> T:
        entity = await self.session.get(self.model, entity_id)
        for key, value in new_data.items():
            setattr(entity, key, value)
        await self.session.flush()
        return entity

    async def _update_by_entity(self, entity: T, **new_data) -> T:
        for key, value in new_data.items():
            setattr(entity, key, value)
        await self.session.flush()
        return entity


class DeletePostgresMixin(BasePostgresMixin[T]):
    async def _delete_by_id(self, entity_id: int):
        entity = await self.session.get(self.model, entity_id)
        await self.session.delete(entity)
        await self.session.flush()

    async def _delete_by_entity(self, entity: T):
        await self.session.delete(entity)
        await self.session.flush()
