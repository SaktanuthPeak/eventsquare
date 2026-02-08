from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from . import jobs

scheduler = AsyncIOScheduler()


def setup_scheduler():

    scheduler.add_job(
        jobs.daily_schedule,
        CronTrigger(hour=0, minute=1),
        id="daily_schedule",
        replace_existing=True,
    )

    logger.info("Scheduler jobs configured")

    return scheduler
