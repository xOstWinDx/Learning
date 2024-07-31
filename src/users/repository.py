from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.repository import AbstractUserRepository
from src.mixins import PostgresReadMixin
from src.models import User


class UserPostgresRepository(PostgresReadMixin[User], AbstractUserRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)
