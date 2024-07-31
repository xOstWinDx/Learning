import jwt
from fastapi import Depends
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.auth.config import AUTH_CONFIG
from src.auth.repository import AuthPostgresRepository
from src.auth.service import AuthService
from src.auth.utils import encode_jwt

from src.auth.exceptions import InvalidCredentialsAuthExc, UnknownUserAuthExc, InvalidTokenAuthExc
from src.exceptions import ForbiddenAuthExc
from src.auth.schemas import UserAuth, JwtPayload
from src.database import get_async_session
from src.models import User


async def authentication(
        user_auth: UserAuth,
        session: AsyncSession = Depends(get_async_session)
) -> str:
    auth_service = AuthService(AuthPostgresRepository(session=session))
    user = await auth_service.get_one_or_none(email=user_auth.email)
    if not user or not user.check_password(user_auth.password):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayload(id=user.id, name=user.name))


def decode_jwt(request: Request, token: str | None = None) -> JwtPayload:
    cookie_token = request.cookies.get("token")
    if token is None and cookie_token is None:
        raise InvalidTokenAuthExc
    jwt_token = token if token is not None else cookie_token
    try:
        payload = jwt.decode(
            jwt=jwt_token,  # type: ignore
            key=AUTH_CONFIG.JWT_SECRET_KEY,
            algorithms=[AUTH_CONFIG.JWT_ALGORITHM]
        )
        return JwtPayload(**payload)
    except (PyJWTError, ValidationError):
        raise InvalidTokenAuthExc


def authorization(is_admin: bool = False):
    async def inner(
            payload: JwtPayload = Depends(decode_jwt),
            session: AsyncSession = Depends(get_async_session)
    ) -> User:
        auth_service = AuthService(AuthPostgresRepository(session=session))
        user = await auth_service.get_one_or_none(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if is_admin and not user.is_admin:
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
