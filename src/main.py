from fastapi import FastAPI

from src.logging import configure_logger
from src.users import users_router

configure_logger()

app = FastAPI()

app.include_router(users_router)
