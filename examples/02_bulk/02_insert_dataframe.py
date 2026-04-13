import pandas as pd
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

    # 1. Create a Pandas DataFrame
    data = {
        "timestamp": [1700000100, 1700000101, 1700000102],
        "metric_name": ["network_in", "network_out", "errors"],
        "value": [1024.5, 512.2, 0.0],
    }
    df = pd.DataFrame(data)

    # 2. Insert the DataFrame
    # This uses clickhouse-connect's native insert_df method
    print("Inserting data from Pandas DataFrame...")
    db.insert_dataframe(df)

    # 3. Verify
    print(f"Total metrics after DataFrame insert: {db.count()}")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print(
            "Error: pandas is required for this example. Install it with: pip install pandas"
        )
