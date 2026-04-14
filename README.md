# wclickhouse

A high-performance ClickHouse ORM for Python using **Pydantic v2**, **clickhouse-connect**, and **Apache Arrow**.

## Features

- **Pydantic v2 Integration**: Define your ClickHouse tables as Pydantic models with full validation.
- **Apache Arrow Native**: High-speed binary columnar data exchange via `insert_arrow()` and `query_arrow()`.
- **Buffer Manager**: Automatic grouping of small inserts to protect server performance.
- **Query Streaming**: Process millions of rows with low memory footprint using lazy loading.
- **Auto-Sync**: Automatically creates tables and syncs schema (adds missing columns).
- **Dual API**: Full support for both **Synchronous** and **Asynchronous** operations.
- **OLAP Optimized**: Built-in support for bulk insertions and Pandas DataFrames.
- **LTS Version**: Enterprise-grade stability with 95% test coverage.

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
    "password": "test_pass",
    "database": "default"
}

# 3. Initialize (Auto-creates table)
db = WClickHouse(AnalyticsEvent, db_config)

# 4. Bulk Insert (High performance)
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
1. Use **Apache Arrow** for massive ingestion (`insert_arrow`).
2. Enable the **Buffer Manager** for streaming small individual records.
3. Prefer `insert_many()` or `insert_dataframe()` over multiple `insert()` calls.

## Documentation

Full documentation available at [wclickhouse.readthedocs.io](https://wclickhouse.readthedocs.io/) and the interactive landing page `index.html`.

## License

MIT
