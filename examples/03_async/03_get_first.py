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

    # 1. Get first record asynchronously
    print("Fetching first user...")
    user = await db.get_first_async()

    if user:
        print(f"Found: {user.name} ({user.email})")
    else:
        print("No users found.")


if __name__ == "__main__":
    asyncio.run(main())
