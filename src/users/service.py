import uuid
from typing import Sequence

from src.abstract import AbstractService
from src.users.repository import UserRepository
from src.users.schemas import UserAll, UserResponse
from src.users.utils import hash_password


class UserService(AbstractService[UserResponse, UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_id(self, user_id: uuid.UUID) -> UserResponse | None:
        user = await self.repository.get_one_or_none(id=user_id)
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def get_all(
            self,
            id: uuid.UUID | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> Sequence[UserResponse | None]:
        return [
            UserResponse.model_validate(user) for user in await self.repository.get_all(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            )
        ]

    async def get_one_or_none(
            self,
            id: uuid.UUID | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> UserResponse | None:
        user = await self.repository.get_one_or_none(
            id=id,
            email=email,
            name=name,
            is_admin=is_admin
        )
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def add(
            self,
            email: str,
            password: str,
            name: str
    ) -> UserResponse:
        if await self.repository.is_exists(email=email):
            raise ValueError("User already exists")
        return UserResponse.model_validate(
            await self.repository.add(
                id=uuid.uuid4(),
                email=email,
                hashed_password=hash_password(password),
                name=name
            )
        )

    async def is_exists(
            self,
            id: uuid.UUID | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> bool:
        return await self.repository.is_exists(
            id=id,
            email=email,
            name=name,
            is_admin=is_admin
        )

    async def delete(self, entity_id: uuid.UUID) -> None:
        pass
