from typing import Sequence

from src.abstract.repository import AbstractUserRepository

import logging

from src.users.schemas import UserResponse

logger = logging.getLogger("user.service")


class UserService:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def get_one_or_none(self, **filter_by) -> UserResponse | None:
        user = await self.repository.get_one_or_none(**filter_by)
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def get_by_id(self, user_id: int) -> UserResponse | None:
        logger.debug("Get user by id: %s", id)
        try:
            user = await self.repository.get_by_id(entity_id=user_id)
            if user is None:
                logger.warning("User not found: %s", id)
                return None
            logger.info("User found: %s", user)
            return UserResponse.model_validate(user)
        except Exception as e:
            logger.exception("Exception while getting user: %s", e)
            raise

    async def get_all(self, **filter_by) -> Sequence[UserResponse | None]:
        logger.debug("Get users by filters: %s", filter_by)
        try:
            users = await self.repository.get_all(**filter_by)
            if not users:
                logger.debug("Users not found by filters: %s", filter_by)
                return []
            logger.info("Users found: %s", users)
            return [UserResponse.model_validate(user) for user in users]
        except Exception as e:
            logger.exception("Exception while getting users: %s", e)
            raise

    async def is_exists(self, **filter_by) -> bool:
        logger.debug("Check if user exists: %s", filter_by)
        try:
            return await self.repository.is_exists(**filter_by)
        except Exception as e:
            logger.exception("Exception while checking if user exists: %s", e)
            raise

    async def delete(self, user_id: int) -> None:
        logger.debug("Delete user: %s", user_id)
        try:
            return await self.repository.delete_by_id(entity_id=user_id)
        except Exception as e:
            logger.exception("Exception while deleting user: %s", e)
            raise
