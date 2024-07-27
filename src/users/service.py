import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.base import BaseService
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import UserResponse, UserAll
from src.users.utils import hash_password


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_user(
            self,
            email: str,
            password: str,
            name: str
    ) -> None:
        async def operation(session: AsyncSession) -> None:
            user_repo = UserRepository(session=session)
            if await user_repo.is_exists(email=email):
                raise ValueError("User already exists")
            await user_repo.add(
                id=uuid.uuid4(),
                email=email,
                hashed_password=hash_password(password),
                name=name
            )

        await self._execute(operation)

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserAll:
        async def operation(session: AsyncSession) -> User:
            user_repo = UserRepository(session=session)
            return await user_repo.get_one_or_none(id=user_id)

        user = await self._execute(operation)
        return UserAll.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserAll:
        async def operation(session: AsyncSession) -> User:
            user_repo = UserRepository(session=session)
            return await user_repo.get_one_or_none(email=email)

        user = await self._execute(operation)
        return UserAll.model_validate(user)

    async def get_all_users(self) -> list[UserAll]:
        async def operation(session: AsyncSession) -> Sequence[User]:
            user_repo = UserRepository(session=session)
            return await user_repo.get_all()

        users = await self._execute(operation)
        return [UserAll.model_validate(user) for user in users]
