from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.users.auth.dependencies import authorization_admin, authorization, authorization_user
from src.users.auth.exceptions import ForbiddenAuthExc
from src.users.dependencies import get_user_service
from src.users.schemas import UserRead
from src.users.service import UserService

router = APIRouter()


@router.get("/users/{user_id}/", status_code=200, response_model=UserRead)
async def get_user(
        user_id: UUID4,
        user_service: UserService = Depends(get_user_service),
        user=Depends(authorization_user)
):
    if user_id != user.id and not user.is_admin:
        raise ForbiddenAuthExc
    return await user_service.get_user(id=user_id)


@router.get("/users/", status_code=200, response_model=list[UserRead])
async def get_all_user(
        user_service: UserService = Depends(get_user_service),
        _=Depends(authorization_admin)
):
    return await user_service.get_all_users()
