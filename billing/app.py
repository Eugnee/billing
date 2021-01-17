from fastapi import FastAPI
from .config import settings
from aiopg.sa import create_engine

app = FastAPI(debug=settings.DEBUG)


@app.on_event("startup")
async def startup():
    app.db = await create_engine(
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )


@app.on_event("shutdown")
async def shutdown():
    app.db.close()
    await app.db.wait_closed()
