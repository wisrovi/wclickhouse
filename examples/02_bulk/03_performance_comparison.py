import time

from pydantic import BaseModel

from wclickhouse import WClickHouse


class PerformanceMetric(BaseModel):
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

    db = WClickHouse(PerformanceMetric, db_config)
    db.delete_all()  # Clean start

    count = 100
    print(f"--- Running performance comparison for {count} records ---")

    # 1. Single inserts (Not recommended for ClickHouse)
    print("Testing single inserts...")
    start_time = time.time()
    for i in range(count):
        db.insert(PerformanceMetric(id=i, data="test"))
    single_time = time.time() - start_time
    print(f"Single inserts took: {single_time:.4f} seconds")

    db.delete_all()

    # 2. Bulk insert (Highly recommended)
    print("\nTesting bulk insert...")
    metrics = [PerformanceMetric(id=i, data="test") for i in range(count)]
    start_time = time.time()
    db.insert_many(metrics)
    bulk_time = time.time() - start_time
    print(f"Bulk insert took: {bulk_time:.4f} seconds")

    # 3. Conclusion
    if single_time > 0:
        improvement = (single_time / bulk_time) if bulk_time > 0 else 0
        print(f"\nBulk insert was ~{improvement:.1f}x faster!")


if __name__ == "__main__":
    main()
