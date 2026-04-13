import asyncio

from pydantic import BaseModel

from wclickhouse import WClickHouse


class HealthCheck(BaseModel):
    id: int


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }
    db = WClickHouse(HealthCheck, db_config)

    # Use .ping() for simple health check
    print("--- Checking Connectivity ---")
    if db.ping():
        print("Success: ClickHouse is reachable.")
    else:
        print("Error: Could not reach ClickHouse.")

    # Async ping
    async def run_async():
        if await db.ping_async():
            print("Success (Async): ClickHouse is reachable.")

    asyncio.run(run_async())


if __name__ == "__main__":
    main()
