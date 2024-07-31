from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.repository import AbstractAuthRepository
from src.mixins import PostgresReadMixin, PostgresCreateMixin, PostgresExistsMixin
from src.models import User


class AuthPostgresRepository(
    PostgresCreateMixin[User],
    PostgresReadMixin[User],
    PostgresExistsMixin[User],
    AbstractAuthRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)
