import asyncio
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.auth.repository import AuthPostgresRepository
from src.auth.service import AuthService
from src.bot.messages import get_start_msg
from src.database import session_factory
from src.logs import configure_logger


configure_logger()
logger = logging.getLogger("bot.start")

start_router = Router(name="start")


@start_router.message(CommandStart())
async def start(message: Message):
    tasks = []
    try:
        async with session_factory() as session:
            async with session.begin():
                auth_services = AuthService(AuthPostgresRepository(session=session))
                tasks.append(
                    asyncio.create_task(
                        message.bot.send_message(
                            chat_id=message.from_user.id,
                            text=get_start_msg(full_name=message.from_user.full_name),
                        )
                    )
                )
                tasks.append(
                    asyncio.create_task(
                        auth_services.register_by_telegram_id(
                            telegram_id=message.from_user.id,
                            name=message.from_user.full_name
                        )
                    )
                )
                await asyncio.gather(*tasks)
                await session.commit()
    except ValueError:
        logger.warning("User already exists: %s", message.from_user.id)
    except Exception as e:
        await session.rollback()
        logger.exception("Exception while starting bot: %s", e)
        raise
