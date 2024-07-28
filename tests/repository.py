import uuid
from typing import Sequence

from src.abstract import AbstractRepository


class InMemoryRepository(AbstractRepository):
    def __init__(self, model):
        super().__init__(model)
        self.entities = []

    async def add(self, **entity_data):
        self.entities.append(self.model(**entity_data))

    async def get_one_or_none(self, **filter_by):
        pass

    async def update(self, entity_id: uuid.UUID, **entity_data):
        pass

    async def get_all(self, **filter_by) -> Sequence:
        pass

    async def is_exists(self, **filter_by) -> bool:
        pass

    async def delete(self, entity_id: uuid.UUID) -> None:
        pass