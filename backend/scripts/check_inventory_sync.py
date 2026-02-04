#!/usr/bin/env python3
"""Check if Redis inventory is in sync with database."""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from api_app.api.core.config import settings
from api_app.api.core.redis import RedisClient
from api_app import models


async def check_inventory_sync(event_id: str):
    """Check inventory sync between Redis and MongoDB."""

    # Connect to MongoDB
    mongo_url = f"mongodb://{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    client = AsyncIOMotorClient(mongo_url)
    await init_beanie(
        database=client[settings.DB_NAME],
        document_models=[models.Event, models.User, models.UserTicket],
    )
    print(f"✅ Connected to MongoDB")

    # Connect to Redis
    redis_client = RedisClient()
    redis = await redis_client.connect()
    print(f"✅ Connected to Redis\n")

    # Get event
    event = await models.Event.get(event_id)
    if not event:
        print(f"❌ Event not found: {event_id}")
        return

    print(f"📊 Event: {event.name} ({event_id})")
    print("=" * 80)

    has_mismatch = False

    for ticket_type in event.ticket_types:
        redis_key = f"inventory:event:{event_id}:ticket:{ticket_type.ticket_id}"
        redis_value = await redis.get(redis_key)

        db_remaining = ticket_type.remaining
        redis_remaining = int(redis_value) if redis_value else None

        status = "✅" if redis_remaining == db_remaining else "❌"

        if redis_remaining != db_remaining:
            has_mismatch = True

        print(f"\n{status} {ticket_type.name} ({ticket_type.ticket_id})")
        print(f"   DB:    {db_remaining} tickets")
        print(f"   Redis: {redis_remaining} tickets")
        print(f"   Diff:  {(redis_remaining or 0) - db_remaining}")

        # Check bookings
        bookings = await models.UserTicket.find(
            models.UserTicket.event.id == event.id,
            models.UserTicket.ticket_type_id == ticket_type.ticket_id,
        ).to_list()

        total_booked = sum(b.quantity for b in bookings)
        expected_remaining = ticket_type.total - total_booked

        print(f"   Total: {ticket_type.total}")
        print(f"   Booked (from user_tickets): {total_booked}")
        print(f"   Expected remaining: {expected_remaining}")

        if db_remaining != expected_remaining:
            print(f"   ⚠️  DB inconsistent! Should be {expected_remaining}")

    print("\n" + "=" * 80)

    if has_mismatch:
        print("❌ Redis and DB are OUT OF SYNC!")
        print("\nTo fix, run:")
        print(f"   curl -X POST http://localhost:8000/api/v1/tickets/{event_id}/sync")
    else:
        print("✅ Redis and DB are in sync!")

    await redis_client.disconnect()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scripts/check_inventory_sync.py <event_id>")
        sys.exit(1)

    event_id = sys.argv[1]
    asyncio.run(check_inventory_sync(event_id))
