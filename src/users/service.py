from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.base import BaseService
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserRead


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session_factory: async_sessionmaker):
        super().__init__(session_factory)

    async def create_user(self, user_data: UserCreate) -> None:
        async def operation(session: AsyncSession) -> None:
            user_repo = UserRepository(session=session)
            if await user_repo.is_exists(email=user_data.email):
                raise ValueError("User already exists")
            await user_repo.add(**user_data.model_dump())

        await self._execute_transaction(operation)

    async def get_user(self, **filter_by):
        async def operation(session: AsyncSession) -> User:
            user_repo = UserRepository(session=session)
            return await user_repo.get_one_or_none(**filter_by)

        user = await self._execute_transaction(operation)
        return user

    async def get_all_users(self) -> list[UserRead]:
        async def operation(session: AsyncSession) -> Sequence[User]:
            user_repo = UserRepository(session=session)
            return await user_repo.get_all()

        users = await self._execute_transaction(operation)
        return [UserRead.model_validate(user) for user in users]
