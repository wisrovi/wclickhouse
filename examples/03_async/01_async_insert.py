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

    # 1. Prepare multiple records
    logs = [
        LogEntry(id=1, message="Server started", level="INFO"),
        LogEntry(id=2, message="Low disk space", level="WARNING"),
    ]

    # 2. Asynchronous insert many
    print(f"Async inserting {len(logs)} logs...")
    await db.insert_many_async(logs)

    # 3. Asynchronous single insert
    print("Async inserting single log...")
    await db.insert_async(LogEntry(id=3, message="Backup completed", level="SUCCESS"))

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
