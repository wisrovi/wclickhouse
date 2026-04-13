from pydantic import BaseModel

from wclickhouse import WClickHouse


# 1. Define your model
class User(BaseModel):
    user_id: int
    name: str
    email: str
    age: int


def main():
    # 2. ClickHouse configuration
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 3. Initialize repository
    # This automatically creates the table 'user'
    db = WClickHouse(User, db_config)

    # 4. Create a record
    new_user = User(user_id=1, name="John Doe", email="john@example.com", age=30)

    # 5. Insert the record
    print(f"Inserting user: {new_user.name}")
    db.insert(new_user)

    print("Done!")


if __name__ == "__main__":
    main()
