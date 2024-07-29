import logging
from typing import Sequence

from src.abstract import AbstractService
from src.common.repository import UserRepository
from src.common.schemas import UserResponse
from src.common.utils import hash_password

logger = logging.getLogger("common.service.user")


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

    async def create_by_telegram_id(
            self,
            telegram_id: int,  # noqa
            name: str,
            password: str | None = None,
    ):
        if await self.is_exists(telegram_id=telegram_id):
            raise ValueError(f"User with id: {telegram_id} already exists")
        return await self.create(name=name, telegram_id=telegram_id, password=password)

    async def create_by_email(
            self,
            email: str,
            name: str,
            password: str | None = None,
    ):
        if await self.is_exists(email=email):
            raise ValueError(f"User with email: {email} already exists")
        return await self.create(name=name, email=email, password=password)

    async def create(
            self,
            name: str,
            email: str | None = None,
            telegram_id: int | None = None,  # noqa
            password: str | None = None,
    ) -> UserResponse:
        logger.debug("Add user: %s", id)
        if password is not None:
            password = hash_password(password)
        try:
            return UserResponse.model_validate(
                await self.repository.create(
                    telegram_id=telegram_id,
                    email=email,
                    name=name,
                    hashed_password=password
                )
            )
        except Exception as e:
            logger.exception("Exception while adding user: %s", e)
            raise

    async def is_exists(
            self,
            id: int | None = None,  # noqa
            telegram_id: int | None = None,
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
                telegram_id=telegram_id,
                email=email,
                name=name,
                is_admin=is_admin
            )
        except Exception as e:
            logger.exception("Exception while checking if user exists: %s", e)
            raise

    async def delete(self, entity_id: int) -> None:
        pass
