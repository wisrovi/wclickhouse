import asyncio

from pydantic import BaseModel, ValidationError, Field

from wclickhouse import WClickHouse


class UserProfile(BaseModel):
    username: str
    age: int = Field(gt=0, lt=150) # Age must be between 1 and 149


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(UserProfile, db_config)

    print("--- Inserting valid data ---")
    db.insert_one(UserProfile(username="alice", age=25))

    print("--- Attempting to insert invalid data (Pydantic Validation) ---")
    try:
        # This will fail at the model creation level (Pydantic v2)
        invalid_user = UserProfile(username="bob", age=-5)
        db.insert_one(invalid_user)
    except ValidationError as e:
        print(f"Caught expected Pydantic ValidationError: {e.error_count()} errors found.")
        # print(e.json())

    print("\n--- Attempting to insert invalid data type (Manual Dict) ---")
    try:
        # WClickHouse expects the model instances for insert methods.
        # If we bypass the model constructor, Pydantic might still catch it 
        # depending on internal library implementation of WClickHouse.
        db.insert_many([{"username": "charles", "age": "not_a_number"}])
    except Exception as e:
        print(f"Caught generic exception during insert: {type(e).__name__}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
