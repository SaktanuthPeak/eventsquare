import asyncio
import logging
import json
import datetime

logger = logging.getLogger(__name__)


class ControllerServer:
    def __init__(self, settings):
        self.settings = settings
        self.running = False

    async def run_daily(self):
        time_check = self.settings.DAILY_TIME_TO_RUN_QUEUE
        hour, minute = time_check.split(":")
        process_time = datetime.time(int(hour), int(minute), 0)

        # ===== first time run something after initial here =====
        # --->
        logger.debug("---> start first time run")
        # =======================================================

        # run loop
        while self.running:
            date = datetime.date.today()
            time_set = datetime.datetime.combine(date, process_time)
            time_to_check = time_set - datetime.datetime.now()

            await asyncio.sleep(time_to_check.seconds)
            logger.debug("start run daily")

            # ============= do something here =============
            # --->
            # =============================================

            await asyncio.sleep(10)
            logger.debug("end run daily")

    async def set_up(self):
        logging.basicConfig(
            format="%(asctime)s - %(name)s:%(levelname)s:%(lineno)d - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.DEBUG,
        )

    def run(self):
        self.running = True
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(self.set_up())
        daily_run = loop.create_task(self.run_daily())

        try:
            loop.run_forever()
        except Exception as e:
            self.running = False
        finally:
            loop.close()
