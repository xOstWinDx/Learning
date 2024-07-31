import logging

from src.abstract.repository import AbstractAuthRepository
from src.auth.utils import hash_password

logger = logging.getLogger("auth.service")


class AuthService:
    def __init__(self, repository: AbstractAuthRepository):
        self.repository = repository

    async def get_one_or_none(self, **filter_by):
        return await self.repository.get_one_or_none(**filter_by)

    async def register_by_telegram_id(
            self,
            telegram_id: int,
            name: str,
            password: str | None = None,
    ):
        if await self.is_exists(telegram_id=telegram_id):
            raise ValueError(f"User with id: {telegram_id} already exists")
        return await self.__register(name=name, telegram_id=telegram_id, password=password)

    async def register_by_email(
            self,
            email: str,
            name: str,
            password: str | None = None,
    ):
        if await self.is_exists(email=email):
            raise ValueError(f"User with email: {email} already exists")
        return await self.__register(name=name, email=email, password=password)

    async def __register(
            self,
            name: str,
            email: str | None = None,
            telegram_id: int | None = None,  # noqa
            password: str | None = None,
            is_admin: bool = False
    ) -> None:
        logger.debug("Add user: %s", id)
        if password is not None:
            password = hash_password(password)
        try:
            await self.repository.create_by_data(
                telegram_id=telegram_id,
                email=email,
                name=name,
                hashed_password=password,
                is_admin=is_admin
            )
        except Exception as e:
            logger.exception("Exception while adding user: %s", e)
            raise

    async def is_exists(self, **filter_by) -> bool:
        logger.debug("Check if user exists: %s", filter_by)
        try:
            return await self.repository.is_exists(**filter_by)
        except Exception as e:
            logger.exception("Exception while checking if user exists: %s", e)
            raise
