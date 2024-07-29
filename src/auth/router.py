from asyncio import TaskGroup

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.auth.dependencies import get_async_session
from src.auth.dependencies import authentication
from src.common.repository import UserRepository
from src.common.schemas import UserCreate
from src.common.service import UserService

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201)
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        async with session.begin():
            async with TaskGroup() as tg:
                user_services = UserService(repository=UserRepository(session=session))
                f1 = tg.create_task(
                    user_services.create_by_email(
                        email=user_data.email,
                        name=user_data.name,
                        password=user_data.password
                    )
                )
            # Дополнительная бизнес-логика во время создания юзера...
            await session.commit()
            return f1.result()
    except ExceptionGroup as e:
        await session.rollback()
        for sub_exception in e.exceptions:
            if isinstance(sub_exception, ValueError):
                raise HTTPException(status_code=409, detail=str(sub_exception))
            else:
                print(sub_exception)
                raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(
        response: Response,
        token: str = Depends(authentication)
):
    response.set_cookie("token", token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
