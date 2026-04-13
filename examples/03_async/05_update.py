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

    # 1. Asynchronous update
    # In ClickHouse, this is a mutation: ALTER TABLE ... UPDATE
    print("Updating user age for user_id=1...")
    await db.update_async("user_id = 1", age=31)

    print("Update mutation started!")


if __name__ == "__main__":
    asyncio.run(main())
