import jwt
from fastapi.encoders import jsonable_encoder
from jwt import PyJWTError
from fastapi import Depends, Cookie
from pydantic import ValidationError
from starlette.requests import Request

from src.users.auth.exceptions import InvalidTokenAuthExc, UnknownUserAuthExc, ForbiddenAuthExc, \
    InvalidCredentialsAuthExc
from src.users.auth.schemas import JwtPayload, UserAuth
from src.users.auth.config import AUTH_CONFIG
from src.users.auth.utils import verify_password
from src.users.dependencies import get_user_service
from src.users.models import User
from src.users.service import UserService


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
            jwt=token,
            key=AUTH_CONFIG.JWT_SECRET_KEY,
            algorithms=AUTH_CONFIG.JWT_ALGORITHM
        )
        return JwtPayload(**payload)
    except (PyJWTError, ValidationError) as e:
        print(e)
        raise InvalidTokenAuthExc


async def authentication(
        user_auth: UserAuth,
        auth_service: UserService = Depends(get_user_service)
) -> str:
    user = await auth_service.get_user(email=user_auth.email)
    if not (user and verify_password(user_auth.password, user.hashed_password)):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayload(id=user.id, name=user.name))


def authorization(is_admin: bool = False):
    async def inner(
            payload: JwtPayload = Depends(decode_jwt),
            auth_service: UserService = Depends(get_user_service)
    ) -> User:
        user = await auth_service.get_user(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if not (user.is_admin == is_admin):
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
