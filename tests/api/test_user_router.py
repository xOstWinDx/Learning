import pytest
from httpx import AsyncClient


async def test_get_users(
        unauthorized_client: AsyncClient,
        authorized_client: AsyncClient,
        admin_client: AsyncClient
) -> None:
    unauth_response = await unauthorized_client.get("/users/")
    base_response = await authorized_client.get("/users/")
    admin_response = await admin_client.get("/users/")

    assert unauth_response.status_code == 401
    assert base_response.status_code == 403
    assert admin_response.status_code == 200


@pytest.mark.parametrize(
    "unauth_status, base_status, admin_status, user_id",
    [
        (401, 403, 200, 1),
        (401, 200, 200, 2),
        (401, 403, 404, 999)
    ]
)
async def test_get_user(
        unauthorized_client: AsyncClient,
        authorized_client: AsyncClient,
        admin_client: AsyncClient,
        unauth_status: int,
        base_status: int,
        admin_status: int,
        user_id: int
) -> None:
    unauth_response = await unauthorized_client.get(f"/users/{user_id}/")
    base_response = await authorized_client.get(f"/users/{user_id}/")
    admin_response = await admin_client.get(f"/users/{user_id}/")

    assert unauth_response.status_code == unauth_status
    assert base_response.status_code == base_status
    assert admin_response.status_code == admin_status
