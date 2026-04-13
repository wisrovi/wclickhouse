from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define your model
class Product(BaseModel):
    __tablename__ = "upsert_product"
    product_id: int
    name: str
    price: float
    version: int

def main():
    # 2. ClickHouse configuration
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 3. Force clean start to ensure ReplacingMergeTree is used
    from wclickhouse import get_client
    client = get_client(db_config)
    client.command("DROP TABLE IF EXISTS upsert_product")

    # 4. Initialize repository with ReplacingMergeTree engine
    db = WClickHouse(
        Product,
        db_config,
        engine="ReplacingMergeTree(version) ORDER BY product_id"
    )

    # 5. Insert initial record
    print("Inserting initial product...")
    db.insert(Product(product_id=1, name="Laptop", price=1200.0, version=1))

    # 6. Insert "updated" record (Upsert behavior)
    print("Upserting product with new price and higher version...")
    db.insert(Product(product_id=1, name="Laptop", price=1150.0, version=2))

    # 7. Use FINAL to see the deduplicated results immediately
    print("\nFetching products with FINAL (guaranteed deduplication):")
    final_products = db.query(f"SELECT * FROM {db.table_name} FINAL")
    for p in final_products:
        print(f"ID: {p.product_id}, Name: {p.name}, Price: {p.price}, Version: {p.version}")

    print("\nDone!")

if __name__ == "__main__":
    main()
