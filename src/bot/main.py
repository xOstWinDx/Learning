import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.bot.config import BOT_CONFIG
from src.bot.routers import start_router

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_CONFIG.TOKEN,
    default=DefaultBotProperties(parse_mode='html')
)

dp = Dispatcher()
dp.include_router(start_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
