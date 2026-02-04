"""Redis distributed lock for handling race conditions.

Monitoring Redis Operations:
    # Monitor all Redis operations in real-time
    docker exec redis-stack redis-cli MONITOR

    # View Redis info and statistics
    docker exec redis-stack redis-cli INFO

    # List all inventory keys
    docker exec redis-stack redis-cli KEYS "inventory:*"

    # Get specific inventory value
    docker exec redis-stack redis-cli GET "inventory:event:EVENT_ID:ticket:TICKET_ID"

    # List all lock keys
    docker exec redis-stack redis-cli KEYS "lock:*"
"""

import asyncio
import uuid
from typing import Optional
from redis.asyncio import Redis
from loguru import logger


class RedisLock:
    """Distributed lock implementation using Redis."""

    def __init__(
        self, redis: Redis, key: str, timeout: int = 10, retry_delay: float = 0.1
    ):
        """
        Initialize Redis lock.

        Args:
            redis: Redis client
            key: Lock key (e.g., "lock:event:123:ticket:VIP")
            timeout: Lock timeout in seconds
            retry_delay: Delay between retries in seconds
        """
        self.redis = redis
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.identifier = str(uuid.uuid4())
        self._locked = False

    async def acquire(self, blocking: bool = True, max_retries: int = 100) -> bool:
        """
        Acquire lock.

        Args:
            blocking: Wait for lock if True, return immediately if False
            max_retries: Maximum number of retry attempts

        Returns:
            True if lock acquired, False otherwise
        """
        retries = 0

        while retries < max_retries:
            # Try to set lock with NX (only if not exists) and EX (expiration)
            acquired = await self.redis.set(
                self.key, self.identifier, ex=self.timeout, nx=True
            )

            if acquired:
                self._locked = True
                logger.debug(f"Lock acquired: {self.key} by {self.identifier}")
                return True

            if not blocking:
                return False

            # Wait before retry
            await asyncio.sleep(self.retry_delay)
            retries += 1

        logger.warning(
            f"Failed to acquire lock: {self.key} after {max_retries} retries"
        )
        return False

    async def release(self) -> bool:
        """
        Release lock.

        Returns:
            True if lock released, False if lock not owned
        """
        if not self._locked:
            return False

        # Lua script to ensure we only delete our own lock
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """

        result = await self.redis.eval(lua_script, 1, self.key, self.identifier)

        if result:
            self._locked = False
            logger.debug(f"Lock released: {self.key} by {self.identifier}")
            return True
        else:
            logger.warning(
                f"Failed to release lock: {self.key} - not owned by {self.identifier}"
            )
            return False

    async def __aenter__(self):
        """Context manager entry."""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.release()
        return False


class TicketInventory:
    """Handle ticket inventory with Redis to prevent race conditions."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def _get_ticket_key(self, event_id: str, ticket_type_id: str) -> str:
        """Get Redis key for ticket inventory."""
        return f"inventory:event:{event_id}:ticket:{ticket_type_id}"

    def _get_lock_key(self, event_id: str, ticket_type_id: str) -> str:
        """Get lock key for ticket booking."""
        return f"event:{event_id}:ticket:{ticket_type_id}"

    async def initialize_inventory(
        self, event_id: str, ticket_type_id: str, total_tickets: int
    ) -> bool:
        """
        Initialize ticket inventory in Redis.

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID
            total_tickets: Total available tickets

        Returns:
            True if initialized successfully
        """
        key = self._get_ticket_key(event_id, ticket_type_id)

        # Check if already exists
        existing = await self.redis.get(key)
        if existing is not None:
            logger.debug(f"Inventory already exists: {key} = {existing}")
            return False

        # Set the inventory value
        await self.redis.set(key, str(total_tickets))

        # Verify it was set correctly
        verify = await self.redis.get(key)
        logger.info(
            f"Initialized inventory: {key} = {total_tickets} (verified: {verify})"
        )

        return True

    async def get_available_tickets(
        self, event_id: str, ticket_type_id: str
    ) -> Optional[int]:
        """
        Get number of available tickets.

        Returns:
            Number of tickets or None if not found
        """
        key = self._get_ticket_key(event_id, ticket_type_id)
        count = await self.redis.get(key)

        if count is None:
            logger.warning(f"Inventory not found for key: {key}")
            return None

        try:
            count_int = int(count)
            logger.debug(f"Available tickets for {key}: {count_int}")
            return count_int
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid inventory value for {key}: {count} - Error: {e}")
            return None

    async def reserve_tickets(
        self, event_id: str, ticket_type_id: str, quantity: int, user_id: str
    ) -> dict:
        """
        Reserve tickets with distributed lock to prevent race condition.

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID
            quantity: Number of tickets to reserve
            user_id: User ID making reservation

        Returns:
            dict with status and details
        """
        lock_key = self._get_lock_key(event_id, ticket_type_id)
        inventory_key = self._get_ticket_key(event_id, ticket_type_id)

        # Acquire distributed lock
        async with RedisLock(self.redis, lock_key, timeout=5) as lock:
            # Get current available tickets
            available = await self.redis.get(inventory_key)

            logger.debug(
                f"Reserve attempt: event={event_id}, ticket={ticket_type_id}, "
                f"quantity={quantity}, current_available={available}"
            )

            if available is None:
                logger.error(f"Inventory not initialized for: {inventory_key}")
                return {
                    "success": False,
                    "error": "Ticket type not found or inventory not initialized",
                    "available": 0,
                }

            try:
                available = int(available)
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid inventory value: {available} - Error: {e}")
                return {
                    "success": False,
                    "error": "Invalid inventory data",
                    "available": 0,
                }

            # Check if enough tickets available
            if available < quantity:
                logger.warning(
                    f"Insufficient tickets: event={event_id}, "
                    f"ticket={ticket_type_id}, requested={quantity}, available={available}"
                )
                return {
                    "success": False,
                    "error": "Insufficient tickets",
                    "available": available,
                    "requested": quantity,
                }

            # Deduct tickets using atomic operation
            new_count = await self.redis.decrby(inventory_key, quantity)

            # Verify the deduction
            verify = await self.redis.get(inventory_key)
            logger.info(
                f"Tickets reserved: event={event_id}, ticket={ticket_type_id}, "
                f"quantity={quantity}, remaining={new_count} (verified: {verify}), user={user_id}"
            )

            return {
                "success": True,
                "reserved": quantity,
                "remaining": new_count,
                "event_id": event_id,
                "ticket_type_id": ticket_type_id,
                "user_id": user_id,
            }

    async def release_tickets(
        self,
        event_id: str,
        ticket_type_id: str,
        quantity: int,
        reason: str = "cancelled",
    ) -> dict:
        """
        Release reserved tickets back to inventory.

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID
            quantity: Number of tickets to release
            reason: Reason for release

        Returns:
            dict with status
        """
        lock_key = self._get_lock_key(event_id, ticket_type_id)
        inventory_key = self._get_ticket_key(event_id, ticket_type_id)

        async with RedisLock(self.redis, lock_key, timeout=5):
            # Add tickets back using atomic operation
            new_count = await self.redis.incrby(inventory_key, quantity)

            logger.info(
                f"Tickets released: event={event_id}, ticket={ticket_type_id}, "
                f"quantity={quantity}, new_total={new_count}, reason={reason}"
            )

            return {
                "success": True,
                "released": quantity,
                "available": new_count,
                "reason": reason,
            }

    async def sync_from_database(
        self, event_id: str, ticket_type_id: str, remaining_tickets: int
    ) -> bool:
        """
        Sync inventory from database (use when Redis data is lost).

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID
            remaining_tickets: Current remaining tickets from database

        Returns:
            True if synced successfully
        """
        key = self._get_ticket_key(event_id, ticket_type_id)
        await self.redis.set(key, remaining_tickets)

        logger.info(f"Synced inventory from DB: {key} = {remaining_tickets}")
        return True


async def create_ticket_reservation(
    redis: Redis, event_id: str, ticket_type_id: str, quantity: int, user_id: str
) -> dict:
    """
    Helper function to reserve tickets.

    Usage:
        from api_app.api.core.redis import get_redis
        from api_app.api.core.redis_lock import create_ticket_reservation

        @router.post("/book-ticket")
        async def book_ticket(
            event_id: str,
            ticket_type_id: str,
            quantity: int,
            user_id: str,
            redis = Depends(get_redis)
        ):
            result = await create_ticket_reservation(
                redis, event_id, ticket_type_id, quantity, user_id
            )

            if result["success"]:
                # Save to database
                # Send confirmation
                return {"message": "Booking successful", "details": result}
            else:
                raise HTTPException(400, result["error"])
    """
    inventory = TicketInventory(redis)
    return await inventory.reserve_tickets(event_id, ticket_type_id, quantity, user_id)
