from .user_model import User

import sys
from typing import Sequence, Type, TypeVar
from inspect import getmembers, isclass
import motor
import beanie
from loguru import logger


DocumentType = TypeVar("DocumentType", bound=beanie.Document)


async def gather_documents() -> Sequence[Type[DocumentType]]:
    """Returns a list of all MongoDB document models defined in `models` module."""

    class_models = getmembers(sys.modules[__name__], isclass)

    for key in [k for k in sys.modules if __name__ in k]:
        class_models.extend(getmembers(sys.modules[key], isclass))

    class_models = list(set(class_models))

    return [
        doc
        for _, doc in class_models
        if issubclass(doc, beanie.Document) and doc.__name__ != "Document"
    ]


class BeanieClient:
    async def init_beanie(self, settings):
        self.settings = settings
        logger.debug(settings.DATABASE_URI)
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.DATABASE_URI, connect=True
        )

        documents = await gather_documents()
        print("Documents >>>")
        for document in documents:
            print(document)
        print(self.client.get_default_database())
        await beanie.init_beanie(
            database=self.client.get_default_database(),
            document_models=documents,
            # recreate_views=True,
        )


async def init_beanie(settings):
    await beanie_client.init_beanie(settings)


beanie_client = BeanieClient()
