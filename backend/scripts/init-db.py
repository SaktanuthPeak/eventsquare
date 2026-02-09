#!/usr/bin/env python3
import sys
import datetime
import asyncio
from api_app import models, schemas
from loguru import logger


async def init_database():
    """Initialize database with sample events and tickets"""

    class Setting:
        def __init__(self):
            self.DATABASE_URI = "mongodb://localhost/eventsquaredb"

    settings = Setting()
    if len(sys.argv) > 1:
        settings.DATABASE_URI = "mongodb://mongodb/eventsquaredb"

    await models.init_beanie(settings)

    logger.info("Database connection initialized")

    # Create admin user if not exists
    admin_user = await models.User.find_one(models.User.username == "admin")
    if not admin_user:
        logger.info("Creating admin user")
        admin_user = models.User(
            email="admin@example.com",
            username="admin",
            password="",
            phone_number="0000000000",
            first_name="admin",
            last_name="system",
            roles=["user", "admin"],
            credit=9999999,
            status="active",
        )
        await admin_user.set_password("p@ssw0rd")
        await admin_user.save()
        logger.info("Admin user created")
    else:
        logger.info("Admin user already exists")

    # Check if events already exist
    existing_events = await models.Event.find().count()
    if existing_events > 0:
        logger.warning(
            f"Found {existing_events} existing events. Skipping event creation."
        )
        logger.info("If you want to recreate events, please clear the database first.")
        return

    # Event types and categories
    event_types = [
        "concert",
        "conference",
        "workshop",
        "festival",
        "sports",
        "exhibition",
    ]

    # Sample event data
    events_data = [
        {
            "name": "Summer Music Festival 2026",
            "description": "Join us for an unforgettable summer music experience with top artists from around the world.",
            "event_type": "festival",
            "location": "Central Park, New York",
        },
        {
            "name": "Tech Innovation Summit",
            "description": "Discover the latest trends in technology and innovation. Network with industry leaders.",
            "event_type": "conference",
            "location": "Convention Center, San Francisco",
        },
        {
            "name": "Jazz Night Live",
            "description": "An evening of smooth jazz performances by renowned artists.",
            "event_type": "concert",
            "location": "Blue Note Jazz Club, New York",
        },
        {
            "name": "Digital Marketing Workshop",
            "description": "Learn effective digital marketing strategies from experts in the field.",
            "event_type": "workshop",
            "location": "Innovation Hub, Austin",
        },
        {
            "name": "International Food Festival",
            "description": "Experience culinary delights from around the globe.",
            "event_type": "festival",
            "location": "Waterfront Plaza, Seattle",
        },
        {
            "name": "Rock Concert Spectacular",
            "description": "The biggest rock bands perform live in an electrifying concert.",
            "event_type": "concert",
            "location": "Madison Square Garden, New York",
        },
        {
            "name": "AI & Machine Learning Conference",
            "description": "Deep dive into artificial intelligence and machine learning technologies.",
            "event_type": "conference",
            "location": "Tech Campus, Boston",
        },
        {
            "name": "Photography Exhibition 2026",
            "description": "Stunning photography collection from award-winning photographers.",
            "event_type": "exhibition",
            "location": "Art Gallery, Los Angeles",
        },
        {
            "name": "Marathon City Run",
            "description": "Annual city marathon for runners of all levels.",
            "event_type": "sports",
            "location": "Downtown, Chicago",
        },
        {
            "name": "Startup Pitch Night",
            "description": "Watch innovative startups pitch their ideas to investors.",
            "event_type": "conference",
            "location": "Startup Incubator, Silicon Valley",
        },
        {
            "name": "Classical Music Evening",
            "description": "Experience the beauty of classical music performed by a symphony orchestra.",
            "event_type": "concert",
            "location": "Symphony Hall, Vienna",
        },
        {
            "name": "Yoga & Wellness Retreat",
            "description": "Rejuvenate your mind and body with yoga and wellness activities.",
            "event_type": "workshop",
            "location": "Wellness Center, Bali",
        },
        {
            "name": "Film Festival 2026",
            "description": "Showcasing independent films from talented filmmakers worldwide.",
            "event_type": "festival",
            "location": "Cinema Complex, Toronto",
        },
        {
            "name": "Basketball Championship Finals",
            "description": "The ultimate showdown in professional basketball.",
            "event_type": "sports",
            "location": "Sports Arena, Los Angeles",
        },
        {
            "name": "Modern Art Exhibition",
            "description": "Contemporary art pieces from emerging and established artists.",
            "event_type": "exhibition",
            "location": "Modern Art Museum, Paris",
        },
        {
            "name": "Cooking Masterclass",
            "description": "Learn to cook gourmet dishes with professional chefs.",
            "event_type": "workshop",
            "location": "Culinary Institute, Lyon",
        },
        {
            "name": "Electronic Music Festival",
            "description": "The biggest electronic music event with world-class DJs.",
            "event_type": "festival",
            "location": "Beach Resort, Ibiza",
        },
        {
            "name": "Business Leadership Summit",
            "description": "Learn from successful business leaders and entrepreneurs.",
            "event_type": "conference",
            "location": "Business Center, London",
        },
        {
            "name": "Tennis Grand Slam",
            "description": "Watch top tennis players compete for the championship title.",
            "event_type": "sports",
            "location": "Tennis Center, Melbourne",
        },
        {
            "name": "Science & Innovation Expo",
            "description": "Explore the latest scientific discoveries and innovations.",
            "event_type": "exhibition",
            "location": "Science Museum, Tokyo",
        },
    ]

    logger.info(f"Creating {len(events_data)} events with 3 ticket types each")

    # Create events with ticket types
    created_count = 0
    for i, event_data in enumerate(events_data, 1):
        # Calculate dates relative to today
        base_date = datetime.datetime.now()

        # Events start from 1 week to 12 weeks in the future
        weeks_ahead = (i % 12) + 1
        start_date = base_date + datetime.timedelta(weeks=weeks_ahead)
        end_date = start_date + datetime.timedelta(days=1)  # 1-day event

        # Booking starts now and ends 1 day before event
        booking_start_date = base_date
        booking_end_date = start_date - datetime.timedelta(days=1)

        # Create 3 different ticket types with varying prices and capacity
        ticket_types = [
            schemas.TicketTypeDB(
                name="Standard",
                total=200,
                remaining=200,
                price=50 + (i * 5),  # Varies by event
            ),
            schemas.TicketTypeDB(
                name="VIP",
                total=50,
                remaining=50,
                price=150 + (i * 10),  # Premium pricing
            ),
            schemas.TicketTypeDB(
                name="Early Bird",
                total=100,
                remaining=100,
                price=30 + (i * 3),  # Discounted price
            ),
        ]

        # Create event
        event = models.Event(
            name=event_data["name"],
            description=event_data["description"],
            event_type=event_data["event_type"],
            location=event_data["location"],
            start_date=start_date,
            end_date=end_date,
            booking_start_date=booking_start_date,
            booking_end_date=booking_end_date,
            ticket_types=ticket_types,
            created_by=admin_user.id,
        )

        await event.save()
        created_count += 1
        logger.info(f"Created event {created_count}/20: {event.name}")

    logger.info(f"Successfully created {created_count} events")
    logger.info("Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_database())
