from enum import Enum
from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define your Enum
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# 2. Define your model using the Enum
class UserProfile(BaseModel):
    user_id: int
    name: str
    role: UserRole  # Maps to String in ClickHouse by default

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # Initialize repository
    db = WClickHouse(UserProfile, db_config)

    # 3. Create records with Enums
    users = [
        UserProfile(user_id=1, name="Alice", role=UserRole.ADMIN),
        UserProfile(user_id=2, name="Bob", role=UserRole.USER),
    ]

    print("Inserting users with Enums...")
    db.insert_many(users)

    # 4. Fetch and verify
    print("Fetching users...")
    all_users = db.get_all()
    for user in all_users:
        print(f"User: {user.name}, Role: {user.role} (type: {type(user.role)})")

    print("\nDone!")

if __name__ == "__main__":
    main()
