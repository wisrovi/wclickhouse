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

    # 1. Delete records
    # Important: In ClickHouse, this is an asynchronous mutation
    print("Deleting user with ID 2...")
    db.delete("user_id = 2")

    # 2. Note on deletes
    print("Delete mutation started.")
    print("For large datasets, it's better to use TTL or partitions for removal.")


if __name__ == "__main__":
    main()
