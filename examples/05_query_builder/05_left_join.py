from typing import Optional
from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define base models
class Category(BaseModel):
    category_id: int
    name: str

class Product(BaseModel):
    product_id: int
    name: str
    category_id: Optional[int] = None
    price: float

# 2. Define a model for the LEFT JOIN result
# Category name might be Nullable if there is no match.
class ProductWithCategory(BaseModel):
    product_name: str
    category_name: Optional[str] = None
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
    cat_db = WClickHouse(Category, db_config)
    prod_db = WClickHouse(Product, db_config)

    cat_db.delete_all()
    prod_db.delete_all()

    cat_db.insert_many([
        Category(category_id=1, name="Electronics"),
    ])

    prod_db.insert_many([
        Product(product_id=1, name="Phone", category_id=1, price=500.0),
        Product(product_id=2, name="Mystery Item", category_id=99, price=0.0), # No matching category
    ])

    # 4. Perform LEFT JOIN using raw SQL
    join_db = WClickHouse(ProductWithCategory, db_config)

    sql = f"""
    SELECT 
        p.name as product_name,
        c.name as category_name,
        p.price as price
    FROM product AS p
    LEFT JOIN category AS c ON p.category_id = c.category_id
    """

    print("Executing LEFT JOIN query...")
    results = join_db.query(sql)

    # 5. Process results
    for row in results:
        cat = row.category_name if row.category_name else "N/A"
        print(f"Product: {row.product_name}, Category: {cat}, Price: ${row.price}")

    print("\nDone!")

if __name__ == "__main__":
    main()
