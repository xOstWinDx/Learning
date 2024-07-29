from typing import AsyncGenerator

import jwt
from fastapi import Depends
from jwt import PyJWTError
from pydantic import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.config import CONFIG

from src.database import session_factory
from src.common.exceptions import UnknownUserAuthExc, ForbiddenAuthExc, InvalidTokenAuthExc
from src.common.repository import UserRepository
from src.common.schemas import UserResponse, JwtPayload
from src.common.service import UserService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def decode_jwt(request: Request, token: str | None = None) -> JwtPayload:
    cookie_token = request.cookies.get("token")
    if token is None and cookie_token is None:
        raise InvalidTokenAuthExc
    jwt_token = token if token is not None else cookie_token
    try:
        payload = jwt.decode(
            jwt=jwt_token,  # type: ignore
            key=CONFIG.JWT_SECRET_KEY,
            algorithms=[CONFIG.JWT_ALGORITHM]
        )
        return JwtPayload(**payload)
    except (PyJWTError, ValidationError):
        raise InvalidTokenAuthExc


def authorization(is_admin: bool = False):
    async def inner(
            payload: JwtPayload = Depends(decode_jwt),
            session: AsyncSession = Depends(get_async_session)
    ) -> UserResponse:
        user_service = UserService(repository=UserRepository(session=session))
        user = await user_service.get_one_or_none(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if is_admin and not user.is_admin:
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
