import asyncio
import pytest
from billing.app import app
from billing.models import metadata
from billing.config import settings
from sqlalchemy import create_engine
from billing.api.router import router
from async_asgi_testclient import TestClient


@pytest.fixture(scope="module")
async def test_client():
    app.include_router(router)
    async with TestClient(app) as ac:
        yield ac


@pytest.fixture(scope="module")
def event_loop():

    loop = asyncio.get_event_loop()

    yield loop


@pytest.fixture(autouse=True)
def clean_tables():
    engine = create_engine(
        f"postgresql://{settings.DB_USER}"
        f":{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    conn = engine.connect()

    for table in metadata.tables.keys():
        conn.execute(f'TRUNCATE "{table}" RESTART IDENTITY CASCADE')
    conn.close()
