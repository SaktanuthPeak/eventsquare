from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi_pagination import add_pagination

from .core.router import init_routers
from .core import http_error, validation_error
from contextlib import asynccontextmanager
from .middlewares.base import init_all_middlewares
from .infrastructure.database import init_beanie
from loguru import logger
from .core.config import get_settings
from dotenv import load_dotenv
import os
from pathlib import Path


def create_app() -> FastAPI:
    # Get project root directory (go up 2 levels from run.py)
    project_root = Path(__file__).resolve().parent.parent

    env_file = ".env.dev" if os.getenv("APP_ENV") == "dev" else ".env"
    env_path = project_root / env_file
    if not env_path.exists():
        env_path = project_root / ".env"

    # Load environment variables from correct path
    load_dotenv(env_path)
    logger.debug(f"Loading env from: {env_path}")
    logger.debug(f"APP_ENV: {os.getenv('APP_ENV')}")

    settings = get_settings()
    settings.configure_logging()

    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
    app.add_exception_handler(HTTPException, http_error.http_error_handler)
    app.add_exception_handler(
        RequestValidationError, validation_error.http422_error_handler
    )
    init_all_middlewares(app, settings=settings)
    app.router.lifespan_context = lifespan

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await init_beanie(settings)  # เปิด comment นี้ด้วย
    init_routers(app, settings)
    use_route_names_as_operation_ids(app)
    add_pagination(app)
    yield


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if hasattr(route, "operation_id"):
            route.operation_id = route.name
