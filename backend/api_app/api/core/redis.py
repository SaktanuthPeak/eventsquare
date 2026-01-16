import redis.asyncio as aioredis
from redis.asyncio import Redis
from typing import Optional
from loguru import logger
from .config import settings


class RedisClient:
    """Redis client wrapper for managing connections."""

    def __init__(self):
        self._redis: Optional[Redis] = None

    async def connect(self) -> Redis:
        """Establish connection to Redis."""
        if self._redis is None:
            try:
                self._redis = await aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=10,
                )
                # Test connection
                await self._redis.ping()
                logger.info(f"Connected to Redis at {settings.REDIS_URL}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return self._redis

    async def disconnect(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            logger.info("Disconnected from Redis")
            self._redis = None

    async def get_client(self) -> Redis:
        """Get Redis client instance."""
        if self._redis is None:
            await self.connect()
        return self._redis


# Global Redis client instance
redis_client = RedisClient()


async def get_redis() -> Redis:
    """Dependency to get Redis client."""
    return await redis_client.get_client()
