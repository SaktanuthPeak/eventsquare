import time
from fastapi import FastAPI, Request
from starlette.responses import Response

from ..core.config import Settings


def init_timing_middleware(app: FastAPI, settings: Settings) -> None:
    """Initialize timing middleware for performance monitoring"""
    
    @app.middleware("http")
    async def _add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = "{:0.6f}".format(process_time)
        return response
