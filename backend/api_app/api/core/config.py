from typing import List, Tuple
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import os

ENV: str = os.getenv("APP_ENV", "")


class Settings(BaseSettings):
    # base
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "eventsquare-backend")
    APP_ENV: str = ENV
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "Eventsquare FastAPI"
    VERSION: str = "0.1.0"

    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "mongodb": "mongodb",
    }

    DB: str = "mongodb"
    DB_HOST: str = "localhost"
    DB_PORT: str = "27017"
    DB_USER: str = ""
    DB_NAME: str = "eventsquaredb"
    DB_PASSWORD: str = ""
    DB_ENGINE: str = DB_ENGINE_MAPPER[DB]
    DATABASE_URI_FORMAT: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    )
    DATABASE_URI: str = ""

    # auth
    SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000  # 10 mins
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days
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
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Build Redis URL if not provided
        if not self.REDIS_URL:
            if self.REDIS_PASSWORD:
                self.REDIS_URL = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            else:
                self.REDIS_URL = (
                    f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
                )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(
            ".env.dev" if "dev" == ENV else ".env" if "prod" == ENV else ".env.test"
        ),
        env_file_encoding="utf-8",
    )


settings = Settings()
