from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define your model with Map fields
# Dict[str, str] in Pydantic v2 maps to ClickHouse Map(String, String) via our updated type mapper.
class Metadata(BaseModel):
    item_id: int
    attributes: dict[str, str]

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 2. Initialize repository
    db = WClickHouse(Metadata, db_config)

    # 3. Create records with Map data
    items = [
        Metadata(
            item_id=1, 
            attributes={"color": "red", "size": "large", "material": "cotton"}
        ),
        Metadata(
            item_id=2, 
            attributes={"os": "linux", "version": "22.04", "arch": "x86_64"}
        ),
    ]

    print("Inserting items with Map data...")
    db.insert_many(items)

    # 4. Fetch and verify
    print("Fetching items...")
    all_items = db.get_all()
    for item in all_items:
        print(f"ID: {item.item_id}, Attributes: {item.attributes}")
        # Show specific key access from Map
        if "color" in item.attributes:
            print(f"  Color: {item.attributes['color']}")

    print("\nDone!")

if __name__ == "__main__":
    main()
