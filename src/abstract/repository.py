import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Sequence

from sqlalchemy import select, exists, delete, update, Executable, Result, Update, Select, Insert
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseModel

T = TypeVar('T', bound=BaseModel)


class AbstractRepository(Generic[T], ABC):

    def __init__(self, model: Type[T]):
        self.model = model

    @abstractmethod
    async def add(self, **entity_data) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity_id: uuid.UUID, **entity_data) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filter_by) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: uuid.UUID) -> None:
        raise NotImplementedError


class AbstractPostgresRepository(AbstractRepository[T], Generic[T], ABC):

    def __init__(self, model: Type[T], session: AsyncSession):
        super().__init__(model)
        self.session = session
        self.base_select_query = select(self.model)
        self.base_exists_query = select(exists(self.model))
        self.base_insert_stmt = insert(self.model)
        self.base_delete_stmt = delete(self.model)
        self.base_update_stmt = update(self.model)

    async def _execute(self, stmt: Executable) -> Result:
        return await self.session.execute(stmt)

    def _query_filters_builder(self, base_query: Select | Insert | Update, **filter_by) -> Select | Insert | Update:
        for key, value in filter_by.items():
            if value is not None:
                base_query = base_query.where(getattr(self.model, key) == value)
        return base_query
