from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_async_session
from src.auth import authorization_admin, authorization_user, ForbiddenAuthExc
from src.users.repository import UserRepository
from src.users.schemas import UserResponse
from src.users.service import UserService

router = APIRouter()


@router.get("/users/{user_id}/", status_code=200, response_model=UserResponse)
async def get_user(
        user_id: UUID4,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(authorization_user)
):
    if user_id != user.id and not user.is_admin:
        raise ForbiddenAuthExc

    user_service = UserService(repository=UserRepository(session=session))
    return await user_service.get_one_or_none(id=user_id)


@router.get("/users/", status_code=200, response_model=list[UserResponse])
async def get_all_user(
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_admin)
):
    user_service = UserService(repository=UserRepository(session=session))
    return await user_service.get_all()
