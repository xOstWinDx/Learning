from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from src.users.dependencies import get_user_service
from src.users.schemas import UserCreate
from src.users.service import UserService

router = APIRouter()


@router.get("/users/{user_id}/", status_code=200)
async def get_user(
        user_id: UUID4,
        user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user(user_id)


@router.post("/users", status_code=201)
async def create_user(
        user_data: UserCreate,
        user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.create_user(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
