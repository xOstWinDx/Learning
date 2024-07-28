import jwt
from jwt import PyJWTError
from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.dependencies import get_async_session
from src.auth.exceptions import InvalidTokenAuthExc, UnknownUserAuthExc, ForbiddenAuthExc, \
    InvalidCredentialsAuthExc
from src.auth.schemas import JwtPayload, UserAuth
from src.auth.config import AUTH_CONFIG
from src.auth.service import AuthService
from src.auth.utils import verify_password
from src.users.repository import UserRepository
from src.users.schemas import UserAll


def encode_jwt(payload: JwtPayload) -> str:
    return jwt.encode(
        payload=payload.model_dump(),
        key=AUTH_CONFIG.JWT_SECRET_KEY,
        algorithm=AUTH_CONFIG.JWT_ALGORITHM
    )


def decode_jwt(request: Request) -> JwtPayload:
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(
            jwt=token,  # type: ignore
            key=AUTH_CONFIG.JWT_SECRET_KEY,
            algorithms=[AUTH_CONFIG.JWT_ALGORITHM]
        )
        return JwtPayload(**payload)
    except (PyJWTError, ValidationError) as e:
        print(e)
        raise InvalidTokenAuthExc


async def authentication(
        user_auth: UserAuth,
        session: AsyncSession = Depends(get_async_session)
) -> str:
    auth_service = AuthService(repository=UserRepository(session=session))
    user = await auth_service.get_one_or_none(email=user_auth.email)
    if not (user and verify_password(user_auth.password, user.hashed_password)):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayload(id=user.id, name=user.name))


def authorization(is_admin: bool = False):
    async def inner(
            payload: JwtPayload = Depends(decode_jwt),
            session: AsyncSession = Depends(get_async_session)
    ) -> UserAll:
        auth_service = AuthService(repository=UserRepository(session=session))
        user = await auth_service.get_one_or_none(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if is_admin and not user.is_admin:
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
