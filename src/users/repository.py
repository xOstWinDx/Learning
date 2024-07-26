from sqlalchemy.ext.asyncio import AsyncSession

from src.base import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)