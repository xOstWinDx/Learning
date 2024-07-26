from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import Response

from src.users.auth.dependencies import authentication
from src.users.dependencies import get_user_service
from src.users.schemas import UserCreate
from src.users.service import UserService

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user_data: UserCreate, user_services: UserService = Depends(get_user_service)):
    try:
        await user_services.create_user(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login")
async def login(response: Response, token: str = Depends(authentication)):
    response.set_cookie("token", token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
