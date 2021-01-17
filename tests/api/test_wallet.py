from tests.helpers import create_new_user_with_wallet
from billing.modules.wallet_history.handlers import get_last_wallet_history_by_wallet_id
from billing.config import settings
import pytest

pytestmark = pytest.mark.asyncio


async def test_wallet_replenishment__ok(test_client):
    new_user = await create_new_user_with_wallet()
    wallet_id = new_user.wallet_id
    user_id = new_user.id
    data = {"cents": 450}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{wallet_id}/replenish",
        json=data,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": wallet_id,
        "user_id": user_id,
        "balance": 450,
    }
    history = await get_last_wallet_history_by_wallet_id(wallet_id)
    assert history["old_balance"] == 0
    assert history["new_balance"] == 450


async def test_wallet_replenishment__no_wallet(test_client):
    wallet_id = 345
    data = {"cents": 450}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{wallet_id}/replenish",
        json=data,
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "incorrect_cents",
    (
        -100,
        None,
    ),
)
async def test_wallet_replenishment__wrong_cents(incorrect_cents, test_client):
    new_user = await create_new_user_with_wallet()
    wallet_id = new_user.wallet_id
    data = {"cents": incorrect_cents}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{wallet_id}/replenish",
        json=data,
    )
    assert response.status_code == 422
