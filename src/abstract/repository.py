from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Sequence

from sqlalchemy import select, exists, delete, update, Update, Select, Insert, Delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseModel
from src.models import User

T = TypeVar('T', bound=BaseModel)


class AbstractRepository(Generic[T], ABC):

    @abstractmethod
    async def create_by_data(self, **entity_data) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, entity_id: int, **new_data) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filter_by) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, entity_id: int) -> None:
        raise NotImplementedError


class AbstractPostgresRepository(AbstractRepository[T], ABC):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.model = model
        self.session: AsyncSession = session
        self.base_select_query: Select = select(self.model)
        self.base_exists_query: Select = select(exists(self.model))
        self.base_insert_stmt: Insert = insert(self.model)
        self.base_delete_stmt: Delete = delete(self.model)
        self.base_update_stmt: Update = update(self.model)

    @abstractmethod
    async def create_by_entity(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update_by_entity(self, entity: T, **new_data) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_entity(self, entity: T) -> None:
        raise NotImplementedError


class AbstractAuthRepository(ABC):

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> User:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_by_data(self, **entity_data) -> User:
        raise NotImplementedError


class AbstractUserRepository(AbstractRepository[User], ABC):
    pass
