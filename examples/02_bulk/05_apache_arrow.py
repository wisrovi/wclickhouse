import pyarrow as pa
from pydantic import BaseModel
from wclickhouse import WClickHouse


class ArrowMetric(BaseModel):
    __tablename__ = "arrow_metrics"
    id: int
    value: float
    category: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(ArrowMetric, db_config)
    db.delete_all()

    # 1. Create data using Apache Arrow Table
    # This is the fastest way to represent columnar data in memory
    print("--- Creating Apache Arrow Table ---")
    data = {
        "id": [1, 2, 3, 4, 5],
        "value": [10.5, 20.0, 15.2, 30.1, 5.5],
        "category": ["A", "B", "A", "C", "B"]
    }
    table = pa.Table.from_pydict(data)

    # 2. Insert using native Arrow support
    print("Inserting data via insert_arrow()...")
    db.insert_arrow(table)

    # 3. Query and get results back as an Arrow Table
    # This avoids the overhead of creating Pydantic objects if you just need raw data
    print("\n--- Querying results as Arrow Table ---")
    result_table = db.query_arrow("SELECT category, avg(value) FROM arrow_metrics GROUP BY category")
    
    # You can easily convert back to a dictionary or use with other tools
    print("Aggregated Results (from Arrow):")
    print(result_table.to_pydict())

    print(f"\nTotal records in DB: {db.count()}")


if __name__ == "__main__":
    main()
