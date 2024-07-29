from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import encode_jwt
from src.database import session_factory
from src.auth.exceptions import InvalidCredentialsAuthExc
from src.auth.schemas import UserAuth
from src.common.schemas import JwtPayload
from src.auth.service import AuthService
from src.common.repository import UserRepository


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def authentication(
        user_auth: UserAuth,
        session: AsyncSession = Depends(get_async_session)
) -> str:
    auth_service = AuthService(repository=UserRepository(session=session))
    user = await auth_service.get_one_or_none(email=user_auth.email)
    if not user or not user.check_password(user_auth.password):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayload(id=user.id, name=user.name))
