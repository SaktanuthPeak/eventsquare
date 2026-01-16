#!/usr/bin/env python3
"""
Redis Worker CLI
Run background worker to process tasks from Redis queue.

Usage:
    python -m api_app.cmd.worker
"""
import asyncio
from api_app.api.core.redis import redis_client
from api_app.workers.redis_worker import RedisWorker
from loguru import logger
from dotenv import load_dotenv
import os


async def main():
    """Main worker entry point."""
    # Load environment variables
    env_file = ".env.dev" if os.getenv("APP_ENV") == "dev" else ".env"
    load_dotenv(env_file)

    logger.info("Starting Redis Worker...")

    try:
        # Connect to Redis
        redis = await redis_client.connect()

        # Create worker instance
        worker = RedisWorker(redis)

        # Start processing tasks
        await worker.process_tasks()

    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Worker error: {e}")
    finally:
        await redis_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
