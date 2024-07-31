from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract import AbstractPostgresRepository
from src.abstract.repository import AbstractUserRepository
from src.base import BasePostgresRepository
from src.models import User


class UserPostgresRepository(
    BasePostgresRepository[User],
    AbstractPostgresRepository[User],
    AbstractUserRepository,
):
    def __init__(self, session: AsyncSession = None):
        super().__init__(session=session, model=User)



