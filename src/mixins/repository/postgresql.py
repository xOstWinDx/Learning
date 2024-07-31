from typing import Sequence, Type, TypeVar, Generic

from sqlalchemy import select, exists
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract import AbstractReadRepository, AbstractCreateRepository, AbstractExistsRepository
from src.database import BaseModel

T = TypeVar('T', bound=BaseModel)


class BasePostgresMixin(Generic[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model


class PostgresReadMixin(BasePostgresMixin[T], AbstractReadRepository[T]):

    async def get_by_id(self, entity_id: int) -> T:
        return await self.session.get(self.model, entity_id)

    async def get_one_or_none(self, **filter_by) -> T | None:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.one_or_none()

    async def get_all(self, **filter_by) -> Sequence[T]:
        res = await self.session.scalars(
            select(self.model).
            filter_by(**filter_by)
        )
        return res.all()


class PostgresCreateMixin(BasePostgresMixin[T], AbstractCreateRepository[T]):

    async def create_by_data(self, **entity_data) -> int:
        res = await self.session.execute(
            insert(self.model).
            values(**entity_data).
            returning(self.model.id)
        )
        return res.scalar()


class PostgresExistsMixin(BasePostgresMixin[T], AbstractExistsRepository[T]):

    async def is_exists(self, **filter_by) -> bool:
        return await self.session.scalar(
            select(exists(self.model)).
            filter_by(**filter_by)
        )
