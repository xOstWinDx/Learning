import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, name, password, status_code",
    [
        ("alex@mail.com", "Alex", "test_pass_alex", 201),
        ("alex@mail.com", "Alex", "test_pass_alex", 409),
        ("NoAlex@mail.com", "NoAlex", "test_pass_no_alex", 201),
        ("NoAlex@mail.com", "NoAlex", "test_pass_no_alex", 409),
    ]
)
async def test_register(
        email: str,
        name: str,
        password: str,
        status_code: int,
        unauthorized_client: AsyncClient
):
    response = await unauthorized_client.post(
        '/auth/register', json={'email': email, "name": name, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("alex@mail.com", "test_pass_alex", 200),
        ("alex@mail.com", "incorrect_test_pass_alex", 401),
        ("NoAlex@mail.com", "test_pass_no_alex", 200),
        ("NoAlex@mail.com", "incorrect_test_pass_no_alex", 401),
    ]
)
async def test_login(
        authorized_client: AsyncClient,
        email: str,
        password: int,
        status_code: int
):
    response = await authorized_client.post(
        '/auth/login',
        json={
            'email': email,
            'password': password,
        }
    )
    assert response.status_code == status_code
