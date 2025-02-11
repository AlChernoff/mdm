from contextlib import asynccontextmanager

from fastapi import  FastAPI

from mdm.database.database import sessionmanager
from mdm.settings import settings as app_settings
from mdm.device.routes.api import router as device_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Mdm",
    debug=app_settings.server_debug,
    docs_url="/internal/docs",
    openapi_url="/internal/schemas.json",
    redoc_url=None,
    swagger_ui_parameters={
        "persistAuthorization": app_settings.env_name in {"localhost", "dev"},
        "displayRequestDuration": True,
    },
)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


app.include_router(device_router)





if __name__ == "__main__":
    import os

    import fastapi_cli.cli

    fastapi_cli.cli.dev(port=int(os.environ.get("PORT", 8082)))
