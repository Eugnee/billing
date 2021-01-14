import uvicorn
from billing.app import app
from billing.config import settings
from billing.api.router import router


def run_server():
    app.include_router(router)
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
