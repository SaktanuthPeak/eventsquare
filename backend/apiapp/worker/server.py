from arq.connections import RedisSettings
from arq import cron
from ..core.config import get_settings
from .tasks import example_task

class WorkerSettings:
    functions = [example_task] # put job function in this list
    redis_settings = RedisSettings.from_dsn(get_settings().REDIS_URL)
    job_timeout = 7200  # 2 hr
