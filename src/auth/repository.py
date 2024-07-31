from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.repository import AbstractAuthRepository
from src.base import BasePostgresRepository
from src.models import User


class AuthPostgresRepository(AbstractAuthRepository, BasePostgresRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)


