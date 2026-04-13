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

    # 1. Get users by age
    age_to_find = 30
    print(f"Fetching users with age {age_to_find}...")
    users = db.get_by_field(age=age_to_find)

    # 2. Print results
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"- {user.name} ({user.email})")


if __name__ == "__main__":
    main()
