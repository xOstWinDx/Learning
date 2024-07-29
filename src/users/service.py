import logging
import uuid
from typing import Sequence

from src.abstract import AbstractService
from src.users.repository import UserRepository
from src.users.schemas import UserResponse
from src.users.utils import hash_password

logger = logging.getLogger("users.service")


class UserService(AbstractService[UserResponse, UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_id(self, id: int) -> UserResponse | None:  # noqa
        logger.debug("Get user by id: %s", id)
        try:
            user = await self.repository.get_one_or_none(id=id)
            if user is None:
                logger.warning("User not found: %s", id)
                return None
            logger.info("User found: %s", user)
            return UserResponse.model_validate(user)
        except Exception as e:
            logger.exception("Exception while getting user: %s", e)
            raise

    async def get_all(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> Sequence[UserResponse | None]:
        logger.debug(
            "Get users by id: %s, email: %s, name: %s, is_admin: %s",
            id,
            email,
            name,
            is_admin
        )
        try:
            users = await self.repository.get_all(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            )
            if users is None:
                logger.debug(
                    "Users not found by id: %s, email: %s, name: %s, is_admin: %s",
                    id,
                    email,
                    name,
                    is_admin
                )
                return []
            logger.info("Users found: %s", users)
            return [UserResponse.model_validate(user) for user in users]
        except Exception as e:
            logger.exception("Exception while getting users: %s", e)
            raise

    async def get_one_or_none(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> UserResponse | None:
        logger.debug(
            "Get user by id: %s, email: %s, name: %s, is_admin: %s",
            id,
            email,
            name,
            is_admin
        )
        try:
            user = await self.repository.get_one_or_none(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            )
            if user is None:
                logger.debug(
                    "Users not found by id: %s, email: %s, name: %s, is_admin: %s",
                    id,
                    email,
                    name,
                    is_admin
                )
                return None
            return UserResponse.model_validate(user)
        except Exception as e:
            logger.exception("Exception while getting user: %s", e)
            raise

    async def add(
            self,
            id: int,  # noqa
            password: str,
            name: str,
            email: str | None = None,
    ) -> UserResponse:
        logger.debug("Add user: %s", id)
        try:
            if await self.repository.is_exists(id=id) or await self.repository.is_exists(email=email):
                logger.warning("User already exists: %s", id)
                raise ValueError("User already exists")
            return UserResponse.model_validate(
                await self.repository.add(
                    id=id,
                    email=email,
                    hashed_password=hash_password(password),
                    name=name
                )
            )
        except ValueError:
            raise
        except Exception as e:
            logger.exception("Exception while adding user: %s", e)
            raise

    async def is_exists(
            self,
            id: int | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> bool:
        logger.debug(
            "Check if user exists: id: %s email: %s name: %s is_admin: %s",
            id,
            email,
            name,
            is_admin
        )
        try:
            return await self.repository.is_exists(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            )
        except Exception as e:
            logger.exception("Exception while checking if user exists: %s", e)
            raise

    async def delete(self, entity_id: uuid.UUID) -> None:
        pass
