from pydantic import BaseModel

from wclickhouse import WClickHouse


class User(BaseModel):
    user_id: int
    name: str
    email: str
    age: int


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(User, db_config)

    # 1. Update records
    # Important: In ClickHouse, this is an asynchronous mutation
    print("Updating user age...")
    db.update("user_id = 1", age=31)

    # 2. Note on updates
    print(
        "Update mutation started. Mutations in ClickHouse are async and eventually consistent."
    )
    print("You can check mutation progress with: SELECT * FROM system.mutations")


if __name__ == "__main__":
    main()
