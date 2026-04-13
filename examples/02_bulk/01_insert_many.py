from pydantic import BaseModel

from wclickhouse import WClickHouse


class Metric(BaseModel):
    timestamp: int
    metric_name: str
    value: float


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Metric, db_config)

    # 1. Prepare multiple records
    # ClickHouse is designed for high-volume batch inserts
    metrics = [
        Metric(timestamp=1700000000, metric_name="cpu_usage", value=45.2),
        Metric(timestamp=1700000001, metric_name="mem_usage", value=12.5),
        Metric(timestamp=1700000002, metric_name="disk_io", value=1.8),
    ]

    # 2. Bulk insert
    print(f"Inserting {len(metrics)} metrics...")
    db.insert_many(metrics)

    # 3. Verify count
    count = db.count()
    print(f"Total metrics in table: {count}")


if __name__ == "__main__":
    main()
