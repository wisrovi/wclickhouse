from typing import Optional

from pydantic import BaseModel

from wclickhouse import WClickHouse


class Customer(BaseModel):
    customer_id: int
    name: str
    email: Optional[str] = None  # Maps to Nullable(String)
    age: Optional[int] = None  # Maps to Nullable(Int64)


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Customer, db_config)

    # 1. Insert records with and without null values
    customers = [
        Customer(customer_id=1, name="John", email="john@example.com", age=25),
        Customer(customer_id=2, name="Alice", email=None, age=None),
    ]

    print("Inserting customers with nullable fields...")
    db.insert_many(customers)

    # 2. Retrieve and verify
    result = db.get_all()
    for cust in result:
        print(f"Customer: {cust.name}, Email: {cust.email}, Age: {cust.age}")


if __name__ == "__main__":
    main()
