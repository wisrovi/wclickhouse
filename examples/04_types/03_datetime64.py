from datetime import datetime

from pydantic import BaseModel

from wclickhouse import WClickHouse


class Event(BaseModel):
    event_id: int
    event_type: str
    timestamp: datetime  # Maps to DateTime64(3)


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Event, db_config)

    # 1. Record with high-precision timestamp
    event = Event(event_id=501, event_type="LOGIN_SUCCESS", timestamp=datetime.now())

    # 2. Insert record
    print(f"Inserting event with timestamp: {event.timestamp}")
    db.insert(event)

    # 3. Retrieve and verify
    result = db.get_first()
    if result:
        print(f"Retrieved: {result.event_type}")
        print(f"Timestamp: {result.timestamp}")


if __name__ == "__main__":
    main()
