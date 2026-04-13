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

    # Insert sample data if empty
    if db.count() == 0:
        print("Inserting sample users...")
        db.insert_many(
            [
                User(user_id=1, name="John Doe", email="john@example.com", age=30),
                User(user_id=2, name="Jane Smith", email="jane@example.com", age=25),
            ]
        )

    # 1. Retrieve all records
    print("Fetching all users...")
    users = db.get_all()

    # 2. Print results
    for user in users:
        print(f"[{user.user_id}] {user.name} - {user.email}")


if __name__ == "__main__":
    main()
