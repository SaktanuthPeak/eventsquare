import logging
import sys
from typing import Any, Dict, List, Tuple
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

from loguru import logger
from ..utils.logging import InterceptHandler

ENV: str = os.getenv("APP_ENV", "")

# Get project root directory (go up 3 levels from config.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # base
    APP_ENV: str = ENV
    DEBUG: bool = False
    REDIRECT_SLASHES: bool = True
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "IMPs FastAPI"
    VERSION: str = "0.1.0"

    DATABASE_URI: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    # auth
    SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60
    OTP_INTERVAL: int = 30

    API_PREFIX: str = ""

    # CORS
    ALLOW_CREDENTIALS: bool = True
    ALLOW_HOSTS: List[str] = ["*"]
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]
    DISALLOW_AGENTS: List[str] = [
        "zgrab",
        "curl",
        "wget",
        "postmanruntime",
        "python-requests",
    ]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # find query
    DEFAULT_PAGE_SIZE: int = 20
    # MAX_PAGE_SIZE: int = 100

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    DAILY_TIME_TO_RUN_QUEUE: str = "00:00"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(
            PROJECT_ROOT / ".env.dev"
            if "dev" == ENV
            else PROJECT_ROOT / ".env"
            if "prod" == ENV
            else PROJECT_ROOT / ".env.test"
        ),
        env_file_encoding="utf-8",
    )

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """FastAPI application configuration"""
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "version": self.VERSION,
        }

    def configure_logging(self) -> None:
        """Configure application logging"""
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.LOGGING_LEVEL)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.LOGGING_LEVEL}])


@lru_cache
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()


# Export for backward compatibility and convenience
settings = get_settings()
