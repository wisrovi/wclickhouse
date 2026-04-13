# wclickhouse

A high-performance ClickHouse ORM for Python using **Pydantic v2** and **clickhouse-connect**.

## Features

- **Pydantic v2 Integration**: Define your ClickHouse tables as Pydantic models.
- **Auto-Sync**: Automatically creates tables and syncs schema (adds missing columns).
- **Dual API**: Full support for both **Synchronous** and **Asynchronous** operations.
- **Bulk Insert Optimized**: Built-in support for efficient bulk insertions, essential for ClickHouse performance.
- **Type Safety**: Automatic mapping between Python/Pydantic types and ClickHouse analytical types (Arrays, DateTime64, etc.).
- **DataFrames**: Native support for inserting Pandas DataFrames.

## Installation

```bash
pip install wclickhouse
```

## Quick Start

```python
from pydantic import BaseModel
from wclickhouse import WClickHouse
from datetime import datetime
from typing import List

# 1. Define your model
class AnalyticsEvent(BaseModel):
    event_id: int
    event_name: str
    properties: List[str]
    created_at: datetime = datetime.now()

# 2. Configure connection
db_config = {
    "host": "localhost",
    "port": 8124,
    "username": "default",
    "password": "",
    "database": "default"
}

# 3. Initialize (Auto-creates table)
db = WClickHouse(AnalyticsEvent, db_config)

# 4. Bulk Insert (Best for ClickHouse)
events = [
    AnalyticsEvent(event_id=1, event_name="login", properties=["web", "chrome"]),
    AnalyticsEvent(event_id=2, event_name="purchase", properties=["mobile", "ios"])
]
db.insert_many(events)

# 5. Query
results = db.get_all()
print(f"Total events: {len(results)}")
```

## Performance Note

ClickHouse is an OLAP database. For best performance:
1. Prefer `insert_many()` over multiple `insert()` calls.
2. Large batches (1,000 to 100,000 rows) are recommended.
3. Use the `MergeTree` engine (default) for production workloads.

## License

MIT
