from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define model
class Product(BaseModel):
    product_id: int
    name: str
    price: float

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 2. Initialize repository and create sample data
    db = WClickHouse(Product, db_config)
    db.delete_all()

    db.insert_many([
        Product(product_id=1, name="Cheap Pen", price=1.5),
        Product(product_id=2, name="Standard Notebook", price=5.0),
        Product(product_id=3, name="Premium Laptop", price=1500.0),
        Product(product_id=4, name="Expensive Watch", price=500.0),
    ])

    # 3. Perform query with SUBQUERY
    # Objective: Find products with price above average
    sql = f"""
    SELECT * FROM {db.table_name}
    WHERE price > (SELECT avg(price) FROM {db.table_name})
    """

    print("Executing query with subquery...")
    expensive_products = db.query(sql)

    # 4. Process results
    print(f"Products with price above average:")
    for p in expensive_products:
        print(f" - {p.name}: ${p.price}")

    print("\nDone!")

if __name__ == "__main__":
    main()
