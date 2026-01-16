import logging
import sys
from typing import Any, Dict
from functools import lru_cache

from loguru import logger

from ...utils.logging import InterceptHandler
from .config import Settings


class AppSettings(Settings):
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
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
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.LOGGING_LEVEL)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.LOGGING_LEVEL}])

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache
def get_app_settings() -> AppSettings:
    config = AppSettings()
    return config
