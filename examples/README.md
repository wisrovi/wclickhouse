# ClickHouse ORM Examples

This directory contains 30+ examples demonstrating how to use `wclickhouse` with Pydantic v2.

## Categories

### 01_crud
Basic Create, Read, Update, and Delete operations using ClickHouse mutations.
- `01_insert.py`: Single record insertion.
- `02_get_all.py`: Fetching all records from a table.
- `03_get_first.py`: Fetching only the first record.
- `04_get_by_field.py`: Filtering results by field value.
- `05_update.py`: Asynchronous update mutations.
- `06_delete.py`: Asynchronous delete mutations.

### 02_bulk
High-performance ingestion methods essential for ClickHouse.
- `01_insert_many.py`: Fast bulk insertion of Pydantic models.
- `02_insert_dataframe.py`: Native integration with Pandas DataFrames.
- `03_performance.py`: Comparing row-by-row vs bulk insertion speed.

### 03_async
Full asynchronous support for modern Python applications.
- `01_async_insert.py`: Non-blocking insertion.
- `02_async_get_all.py`: Non-blocking retrieval.
- `03_get_first.py`: Async first record retrieval.
- `04_get_by_field.py`: Async filtering.
- `05_update.py`: Async update mutations.
- `06_delete.py`: Async delete mutations.

### 04_types
Mapping ClickHouse specific types to Pydantic models.
- `01_array.py`: Using Python `List[T]` for ClickHouse `Array(T)`.
- `02_nullable.py`: Handling `Optional[T]` as `Nullable(T)`.
- `03_datetime64.py`: High-precision timestamps with `DateTime64`.

### 05_query_builder
Fluent interface for building complex SQL queries.
- `01_simple_select.py`: Basic field selection and limits.
- `02_complex_where.py`: Chaining multiple WHERE conditions.
- `03_group_by_having.py`: Analytical queries with GROUP BY and HAVING.

### 06_analytical
Advanced analytical patterns using ClickHouse power.
- `01_aggregations.py`: Sum, Avg, and Count operations.
- `02_top_k.py`: Finding top items in a dataset.
- `03_timeseries.py`: Time-series aggregation by intervals.

### 07_schema
Automatic management of database structure.
- `01_auto_creation.py`: Table creation from Pydantic models.
- `02_sync_columns.py`: Adding new fields automatically during runtime.

### 08_health
Monitoring and connectivity tools.
- `01_ping.py`: Checking database reachability.
- `02_connectivity.py`: Handling connection errors and retries.

### 09_engines
Leveraging different storage engines.
- `01_memory_engine.py`: Using the fast in-memory engine for transient data.

### 10_advanced
Expert features for production workloads.
- `01_final_modifier.py`: Using the `FINAL` modifier for ReplacingMergeTree engines.

## Running the Examples

1. Start ClickHouse:
   ```bash
   docker-compose up -d
   ```

2. Run any example:
   ```bash
   python examples/01_crud/01_insert.py
   ```
