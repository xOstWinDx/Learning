from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import encode_jwt
from src.common.schemas import JwtPayload
from src.config import CONFIG
from src.common.models import User  # noqa
from src.database import session_factory, engine, BaseModel
from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    assert CONFIG.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    async with session_factory() as session:
        admin_user = User(
            email="admin@admin.com",
            name="Admin",
            is_admin=True,
        )
        base_user = User(
            email="base@base.com",
            name="Base",
            is_admin=False,
        )
        session.add(admin_user)
        session.add(base_user)
        await session.commit()
    yield


@pytest.fixture(scope="session")
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def unauthorized_client() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        client.cookies.set("token", encode_jwt(payload=JwtPayload(id=1, name="Admin")))
        yield client


@pytest.fixture(scope="function")
async def authorized_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        client.cookies.set("token", encode_jwt(payload=JwtPayload(id=2, name="Base")))
        yield client
