import asyncio
import time

from pydantic import BaseModel

from wclickhouse import WClickHouse


class Heartbeat(BaseModel):
    timestamp: int


async def run_with_retry(db_instance, max_retries=3, delay=1):
    """
    Simulates a query with a retry logic if connection is lost
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"--- Attempt {attempt} to count heartbeats ---")
            count = db_instance.count()
            print(f"Success! Total heartbeats: {count}")
            return count
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Giving up.")
                raise e


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Heartbeat, db_config)

    # Insert one record
    db.insert_one(Heartbeat(timestamp=int(time.time())))

    # Run with retry
    await run_with_retry(db)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error in example: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
