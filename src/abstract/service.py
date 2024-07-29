from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence

from pydantic import BaseModel as BMPydantic

from src.abstract.repository import AbstractRepository

R = TypeVar("R", bound=AbstractRepository)
T = TypeVar("T", bound=BMPydantic)


class AbstractService(Generic[T, R], ABC):
    def __init__(self, repository: R):
        self.repository = repository

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filter_by) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, **entity_data) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> T:
        raise NotImplementedError
