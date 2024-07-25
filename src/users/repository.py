from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession


from src.base import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def already_exists(self, email: str) -> bool:
        query = (
            select(exists(self.model)).
            filter_by(email=email)
        )
        res = await self.session.execute(query)
        return res.scalar()
