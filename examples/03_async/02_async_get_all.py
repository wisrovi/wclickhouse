import asyncio

from pydantic import BaseModel

from wclickhouse import WClickHouse


class LogEntry(BaseModel):
    id: int
    message: str
    level: str


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(LogEntry, db_config)

    # 1. Asynchronously retrieve all records
    print("Fetching logs asynchronously...")
    logs = await db.get_all_async()

    # 2. Print results
    print(f"Retrieved {len(logs)} logs.")
    for log in logs:
        print(f"[{log.level}] - {log.message}")


if __name__ == "__main__":
    asyncio.run(main())
