from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.base import BaseService
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserRead


class UserService(BaseService):

    def __init__(self, session_factory: async_sessionmaker):
        super().__init__(session_factory)

    async def create_user(self, user_data: UserCreate) -> None:
        async def operation(session: AsyncSession):
            user_repo = UserRepository(session=session)
            if user_repo.already_exists(email=user_data.email):
                raise ValueError("User already exists")
            return await user_repo.add(model=User(**user_data.model_dump()))

        return await self._execute_transaction(operation)

    async def get_user(self, ident: Any | tuple[Any, ...]) -> UserRead:
        async def operation(session: AsyncSession):
            user_repo = UserRepository(session=session)
            return await user_repo.get(ident=ident)

        return UserRead.model_validate(await self._execute_transaction(operation))
