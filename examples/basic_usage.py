import asyncio
from datetime import datetime

from pydantic import BaseModel

from wclickhouse import WClickHouse


# 1. Define your model with Pydantic v2
class Event(BaseModel):
    event_id: int
    event_type: str
    value: float
    tags: list[str]
    created_at: datetime = datetime.now()


async def main():
    # 2. Database configuration
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 3. Initialize the repository
    # This will automatically create the table 'event' if it doesn't exist
    db = WClickHouse(Event, db_config)

    print("--- Inserting records ---")
    # 4. Insert records (bulk is better for ClickHouse)
    events = [
        Event(event_id=1, event_type="click", value=1.0, tags=["ui", "button"]),
        Event(event_id=2, event_type="view", value=0.0, tags=["page", "landing"]),
    ]
    db.insert_many(events)

    print("--- Querying records ---")
    # 5. Query records
    all_events = db.get_all()
    for event in all_events:
        print(f"ID: {event.event_id}, Type: {event.event_type}, Tags: {event.tags}")

    print("--- Counting records ---")
    count = db.count()
    print(f"Total events: {count}")

    print("--- Async Operations ---")
    await db.insert_async(
        Event(event_id=3, event_type="scroll", value=0.5, tags=["ui"])
    )
    new_count = await db.count_async()
    print(f"Total events after async insert: {new_count}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
