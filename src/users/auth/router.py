import asyncio
from asyncio import TaskGroup

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.dependencies import get_async_session, get_task_group
from src.users.auth.dependencies import authentication
from src.users.schemas import UserCreate
from src.users.service import UserService

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            async with TaskGroup() as tg:
                user_services = UserService(session=session)
                f1 = tg.create_task(
                    user_services.create_user(
                        email=user_data.email,
                        password=user_data.password,
                        name=user_data.name
                    )
                )
                f2 = tg.create_task(asyncio.sleep(5))
                # Дополнительная бизнес-логика во время создания юзера...
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return f1.result(), f2.result()


@router.post("/login")
async def login(
        response: Response,
        token: str = Depends(authentication)
):
    response.set_cookie("token", token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
