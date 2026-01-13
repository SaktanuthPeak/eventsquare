from fastapi import FastAPI
from ..core.config import Settings
from .cors import init_cors_middleware
from .security import init_security_middleware
from .timing import init_timing_middleware


def init_all_middlewares(app: FastAPI, settings: Settings) -> None:
    """Initialize all application middlewares"""
    init_cors_middleware(app, settings)
    init_security_middleware(app, settings)
    init_timing_middleware(app, settings)
