import asyncio

from pydantic import BaseModel

from wclickhouse import WClickHouse


class User(BaseModel):
    user_id: int
    name: str
    email: str
    age: int


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(User, db_config)

    # 1. Get record by field asynchronously
    print("Fetching users with age 30...")
    users = await db.get_by_field_async(age=30)

    print(f"Found {len(users)} users.")
    for user in users:
        print(f" - {user.name} ({user.email})")


if __name__ == "__main__":
    asyncio.run(main())
