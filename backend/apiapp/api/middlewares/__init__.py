import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette import status
from loguru import logger

from ..core.app_settings import AppSettings

def init_middleware(app: FastAPI, settings: AppSettings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
        allow_origins=settings.ALLOW_HOSTS,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")
        logger.debug(f"user-agent ==> {user_agent}")
        for agent in settings.DISALLOW_AGENTS:
            if agent in user_agent.lower():
                logger.warning({"detail": "Client is not allow to uses."})

                return JSONResponse(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    content={"detail": "Client is not allow to uses."},
                )

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = "{:0.6f}".format(process_time)
        return response