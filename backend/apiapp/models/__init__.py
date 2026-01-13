from mongoengine import connect, disconnect_all, DEFAULT_CONNECTION_NAME, Document
from mongoengine.base.common import _get_documents_by_db

from loguru import logger

from .request_log_model import RequestLog
from .token_model import Token

from .user_model import User


__all__ = [
    "RequestLog",
    "Token",
    "User",
]


async def init_mongoengine(settings):
    host = (
        settings.DATABASE_URI_FORMAT
        if settings.DB_USER and settings.DB_PASSWORD
        else "{db_engine}://{host}:{port}/{database}"
    ).format(
        db_engine=settings.DB_ENGINE,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    logger.info("DB URI: " + host)
    get_connection = connect(host=host)
    logger.info("Initialized mongengine")

    return get_connection


async def disconnect_mongoengine():
    disconnect_all()
    logger.info("Closed all mongoengine connections")


cls_documents: list[Document] = _get_documents_by_db(
    DEFAULT_CONNECTION_NAME, DEFAULT_CONNECTION_NAME
)
