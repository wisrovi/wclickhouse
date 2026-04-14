from pydantic import BaseModel
from wclickhouse import WClickHouse


class LargeDataset(BaseModel):
    __tablename__ = "streaming_data"
    id: int
    data: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(LargeDataset, db_config)
    
    # 1. Prepare some data
    print("Preparing 5000 records...")
    batch = [LargeDataset(id=i, data=f"value_{i}") for i in range(5000)]
    db.insert_many(batch)

    # 2. Use query_stream to process rows without loading all into RAM
    print("\n--- Streaming results (Lazy Loading) ---")
    count = 0
    # We only fetch small blocks from the server at a time
    for item in db.query_stream("SELECT * FROM streaming_data"):
        count += 1
        if count % 1000 == 0:
            print(f"  Processed {count} items. Current ID: {item.id}")
            
    print(f"\nFinished streaming {count} records.")


if __name__ == "__main__":
    main()
