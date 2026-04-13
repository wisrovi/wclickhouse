import asyncio
import random

from pydantic import BaseModel

from wclickhouse import WClickHouse


class UserSession(BaseModel):
    user_id: int
    session_id: str


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(UserSession, db_config)

    print("--- Inserting 10,000 sessions for 500 unique users ---")
    sessions = [
        UserSession(user_id=random.randint(1, 500), session_id=f"sess_{i}")
        for i in range(10000)
    ]
    db.insert_many(sessions)

    print("--- Comparing uniqExact() vs uniq() ---")
    # uniqExact() gives the exact number of unique values
    # uniq() uses HyperLogLog++ for a fast approximation
    query = """
    SELECT 
        uniqExact(user_id) as exact_count,
        uniq(user_id) as approx_count
    FROM user_session
    """
    
    from wclickhouse import get_client
    client = get_client(db_config)
    result = client.query(query)
    
    row = result.first_item
    print(f"Exact unique users: {row['exact_count']}")
    print(f"Approximate unique users: {row['approx_count']}")
    
    diff = abs(row['exact_count'] - row['approx_count'])
    print(f"Difference: {diff} (Uniq is faster but less precise on large datasets)")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
