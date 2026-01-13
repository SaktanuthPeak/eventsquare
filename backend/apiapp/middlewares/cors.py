from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from ..core.config import Settings


def init_cors_middleware(app: FastAPI, settings: Settings) -> None:
    """Initialize CORS and compression middlewares"""
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
        allow_origins=settings.ALLOW_HOSTS,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
