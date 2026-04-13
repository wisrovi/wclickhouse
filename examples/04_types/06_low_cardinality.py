from typing import Annotated
from pydantic import BaseModel, Field
from wclickhouse import WClickHouse

# 1. Define your model using ClickHouse manual overrides
# LowCardinality(String) is efficient for strings with low number of unique values.
class Log(BaseModel):
    log_id: int
    level: Annotated[
        str, 
        Field(json_schema_extra={"clickhouse_type": "LowCardinality(String)"})
    ]
    message: str

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 2. Initialize repository
    # This will create the table using the manual override for 'level'
    db = WClickHouse(Log, db_config)

    # 3. Create records
    logs = [
        Log(log_id=1, level="INFO", message="Starting system"),
        Log(log_id=2, level="ERROR", message="Failed to connect"),
        Log(log_id=3, level="INFO", message="User logged in"),
    ]

    print("Inserting logs with LowCardinality string column...")
    db.insert_many(logs)

    # 4. Fetch and verify
    all_logs = db.get_all()
    for log in all_logs:
        print(f"[{log.level}] {log.message}")

    print("\nDone!")

if __name__ == "__main__":
    main()
