from apiapp.infrastructure import database
import logging
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class WorkerTask:
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    async def create(cls, settings):
        await database.init_beanie(settings)
        return cls(settings)


async def init_jobs_context():
    settings = get_settings()
    await database.init_beanie(settings)
    return settings


async def example_task(ctx):
    # do something
    return {"message": "Hello World"}
