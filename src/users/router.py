from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import ForbiddenAuthExc
from src.auth.dependencies import authorization_user, authorization_admin
from src.users.repository import UserPostgresRepository
from src.users.service import UserService, UserResponse

router = APIRouter()


@router.get("/users/{user_id}/", status_code=200, response_model=UserResponse)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(authorization_user)
):
    if user_id != user.id and not user.is_admin:
        raise ForbiddenAuthExc

    user_service = UserService(repository=UserPostgresRepository(session=session))
    if user := await user_service.get_one_or_none(id=user_id):
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/users/", status_code=200, response_model=list[UserResponse | None])
async def get_all_user(
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_admin)
):
    user_service = UserService(repository=UserPostgresRepository(session=session))
    return await user_service.get_all()
