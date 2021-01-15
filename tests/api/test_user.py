from tests.helpers import create_new_user_with_wallet
from billing.config import settings
import pytest

pytestmark = pytest.mark.asyncio


async def test_create_user__ok(test_client):
    data = {"name": "Ivan", "email": "ivanivanov@gmail.com"}
    response = await test_client.post(
        f"{settings.API_PREFIX}/users",
        json=data,
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Ivan",
        "email": "ivanivanov@gmail.com",
        "wallet_id": 1,
        "balance": 0,
    }


async def test_create_user_wrong_data(test_client):
    data = {"name": "Ivan", "email": "ivanivanov"}
    response = await test_client.post(
        f"{settings.API_PREFIX}/users",
        json=data,
    )
    assert response.status_code == 422


async def test_create_user_already_exists(test_client):
    user = await create_new_user_with_wallet()
    data = {"name": "Fake", "email": user["email"]}

    response = await test_client.post(
        f"{settings.API_PREFIX}/users",
        json=data,
    )
    assert response.status_code == 400
