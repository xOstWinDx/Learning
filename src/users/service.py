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
