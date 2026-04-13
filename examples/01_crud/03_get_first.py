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

    # 1. Retrieve the first record
    print("Fetching first user...")
    user = db.get_first()

    # 2. Check if user exists
    if user:
        print(f"First user: {user.name} ({user.email})")
    else:
        print("No users found.")


if __name__ == "__main__":
    main()
