from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define base models
class Category(BaseModel):
    category_id: int
    name: str

class Product(BaseModel):
    product_id: int
    name: str
    category_id: int
    price: float

# 2. Define a model for the JOIN result
class ProductWithCategory(BaseModel):
    product_id: int
    product_name: str
    category_name: str
    price: float

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 3. Initialize repositories and create sample data
    # Note: we use _ to discard the db instances after table creation/population
    cat_db = WClickHouse(Category, db_config)
    prod_db = WClickHouse(Product, db_config)

    cat_db.delete_all()
    prod_db.delete_all()

    cat_db.insert_many([
        Category(category_id=1, name="Electronics"),
        Category(category_id=2, name="Books")
    ])

    prod_db.insert_many([
        Product(product_id=1, name="Phone", category_id=1, price=500.0),
        Product(product_id=2, name="Novel", category_id=2, price=20.0),
    ])

    # 4. Perform INNER JOIN using raw SQL
    # We use a third WClickHouse instance configured with the result model
    join_db = WClickHouse(ProductWithCategory, db_config)

    sql = f"""
    SELECT 
        p.product_id as product_id,
        p.name as product_name,
        c.name as category_name,
        p.price as price
    FROM product AS p
    INNER JOIN category AS c ON p.category_id = c.category_id
    """

    print("Executing INNER JOIN query...")
    results = join_db.query(sql)

    # 5. Process results
    for row in results:
        print(f"Product: {row.product_name}, Category: {row.category_name}, Price: ${row.price}")

    print("\nDone!")

if __name__ == "__main__":
    main()
