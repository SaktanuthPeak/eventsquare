from datetime import datetime, timedelta, UTC
from loguru import logger
from api_app import models
from beanie import PydanticObjectId
from api_app import schemas
from dateutil import tz
from api_app.repositories.user_ticket_repo import UserTicketRepository

LOCAL_TIMEZONE = tz.gettz("Asia/Bangkok")


async def daily_schedule():
    try:
        now = datetime.now(UTC).astimezone(LOCAL_TIMEZONE)
        await daily_update_expired_tickets_status(now)
    except Exception as e:
        logger.error(f"Error in daily status update: {str(e)}")


async def daily_update_expired_tickets_status(now: datetime):
    try:
        user_ticket_repo = UserTicketRepository()
        result = await user_ticket_repo.update_expired_tickets_status(now)
        logger.info(f"Expired tickets updated: {result.modified_count}")
    except Exception as e:
        logger.error(f"Error updating expired tickets: {str(e)}")
