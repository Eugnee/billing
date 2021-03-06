import asyncio
from tests.mocks import get_slow_coro_mock, wallet_mock

from asynctest import mock
from tests.helpers import (
    create_new_user_with_wallet,
    replenish_wallet_with_500_cents,
)
from billing.modules.wallet_history.handlers import get_last_wallet_history_by_wallet_id
from billing.config import settings
import pytest

pytestmark = pytest.mark.asyncio


async def test_wallet_transfer__ok(test_client):
    first_user = await create_new_user_with_wallet()
    first_wallet_id = first_user.wallet_id
    await replenish_wallet_with_500_cents(wallet_id=first_wallet_id)

    second_user = await create_new_user_with_wallet()
    second_wallet_id = second_user.wallet_id
    await replenish_wallet_with_500_cents(wallet_id=second_wallet_id)

    data = {"cents": 342}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{first_wallet_id}/transfer_to/{second_wallet_id}",
        json=data,
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": first_wallet_id,
            "user_id": first_user.id,
            "balance": 158,
        },
        {
            "id": second_wallet_id,
            "user_id": second_user.id,
            "balance": 842,
        },
    ]
    history = await get_last_wallet_history_by_wallet_id(first_wallet_id)
    assert history["old_balance"] == 500
    assert history["new_balance"] == 158

    history = await get_last_wallet_history_by_wallet_id(second_wallet_id)
    assert history["old_balance"] == 500
    assert history["new_balance"] == 842


async def test_wallet_transfer__identical_wallets(test_client):
    wallet_id = 1

    data = {"cents": 342}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{wallet_id}/transfer_to/{wallet_id}",
        json=data,
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "wrong_cents",
    (
        -100,
        None,
    ),
)
async def test_wallet_transfer__wrong_cents(wrong_cents, test_client):
    first_wallet_id = 1
    second_wallet_id = 2
    data = {"cents": wrong_cents}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{first_wallet_id}/transfer_to/{second_wallet_id}",
        json=data,
    )
    assert response.status_code == 422


async def test_wallet_transfer__insufficient_funds(test_client):
    first_user = await create_new_user_with_wallet()
    first_wallet_id = first_user.wallet_id
    await replenish_wallet_with_500_cents(wallet_id=first_wallet_id)

    second_user = await create_new_user_with_wallet()
    second_wallet_id = second_user.wallet_id
    await replenish_wallet_with_500_cents(wallet_id=second_wallet_id)

    data = {"cents": 501}
    response = await test_client.post(
        f"{settings.API_PREFIX}/wallets/{first_wallet_id}/transfer_to/{second_wallet_id}",
        json=data,
    )
    assert response.status_code == 402
    assert response.json() == {"detail": "Insufficient funds on wallet 1"}


async def test_wallet_transfer__race_condition(test_client):
    """trying to get locked rows"""

    first_user = await create_new_user_with_wallet()
    first_wallet_id = first_user.wallet_id

    second_user = await create_new_user_with_wallet()
    second_wallet_id = second_user.wallet_id
    await replenish_wallet_with_500_cents(wallet_id=second_wallet_id)

    with mock.patch(
        "billing.modules.wallet.handlers.update_wallet",
        new_callable=get_slow_coro_mock(return_value=wallet_mock()),
    ):

        data = {"cents": 100}

        async def coro1():
            return await test_client.post(
                f"{settings.API_PREFIX}/wallets/{second_wallet_id}/transfer_to/{first_wallet_id}",
                json=data,
            )

        async def coro2():
            return await test_client.post(
                f"{settings.API_PREFIX}/wallets/{first_wallet_id}/transfer_to/{second_wallet_id}",
                json=data,
            )

        responses = await asyncio.gather(coro1(), coro2())
        status_codes = [r.status_code for r in responses]
        assert 429 in status_codes
