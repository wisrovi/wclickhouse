import asyncio

from pydantic import BaseModel

from wclickhouse import WClickHouse


class LogEntry(BaseModel):
    id: int
    message: str


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
        "settings": {
            "max_execution_time": 2, # Wait max 2 seconds for a query
        }
    }

    db = WClickHouse(LogEntry, db_config)

    print("--- Attempting a long query that exceeds 2 seconds ---")
    # sleep(3) will exceed max_execution_time=2
    query = "SELECT sleep(3) as result"
    
    from wclickhouse import get_client
    client = get_client(db_config)
    
    try:
        # We use client.query which passes settings from db_config to the driver
        result = client.query(query)
        print(f"Results: {result.named_results()}")
    except Exception as e:
        print(f"Caught timeout error: {type(e).__name__}: {e}")
        print("Note: ClickHouse settings.max_execution_time correctly interrupted the query.")

    print("\n--- Running a shorter query (within timeout) ---")
    query_ok = "SELECT sleep(0.5) as result, 'OK' as status"
    try:
        result = client.query(query_ok)
        print(f"Short query results: {result.named_results()}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
