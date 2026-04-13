# ClickHouse ORM Examples

This directory contains **51+ production-ready examples** demonstrating how to use `wclickhouse` with Pydantic v2 across various analytical scenarios.

## Categories

### 01_crud (7 examples)
Basic Create, Read, Update, and Delete operations using ClickHouse mutations and engines.
- `01_insert.py` to `06_delete.py`: Standard CRUD operations.
- `07_replacing_merge_tree_upsert.py`: Professional Upsert pattern using `ReplacingMergeTree` and `FINAL`.

### 02_bulk (3 examples)
High-performance ingestion methods essential for Big Data.
- `01_insert_many.py`: Fast bulk insertion of Pydantic models.
- `02_insert_dataframe.py`: Native integration with Pandas DataFrames (Ultra-fast).
- `03_performance.py`: Real benchmark comparing Row-by-Row vs Bulk methods.

### 03_async (6 examples)
Full non-blocking support for modern Python applications (FastAPI, Starlette).
- Complete async CRUD and connectivity examples.

### 04_types (7 examples)
Advanced mapping between Python/Pydantic and ClickHouse analytical types.
- `Array`, `Nullable`, `DateTime64`, `Enum`, `Decimal`, `LowCardinality`, and `Map`.

### 05_query_builder (7 examples)
Fluent interface for building complex SQL queries.
- Joins (INNER/LEFT), Union All, Subqueries, and complex filters.

### 06_analytical (6 examples)
Master ClickHouse's power for data analysis.
- Aggregations, Top-K, Time-series, Window Functions, and Moving Averages.

### 07_schema (2 examples)
Automatic management of database structure and auto-migrations.

### 08_health (2 examples)
Connectivity checks and health monitoring with `.ping()`.

### 09_engines (1 example)
Using the fast in-memory engine for transient analytical data.

### 10_advanced (1 example)
Expert features like the `FINAL` modifier for collapsing engines.

### 11_error_handling (3 examples)
Robust patterns for catching validation errors, retries, and timeout handling.

### 12_frameworks (1 example)
FastAPI integration using asynchronous dependency patterns.

### 13_advanced_engines (2 examples)
Leveraging `AggregatingMergeTree` and `SummingMergeTree` for automatic background aggregation.

### 14_logging (2 examples)
Integration with `loguru` and performance tracing decorators.

### 15_integrations (1 example)
Efficient conversion from large raw Dict lists to Pydantic models for ingestion.

## Running the Examples

1. Start ClickHouse:
   ```bash
   docker-compose up -d
   ```

2. Run all examples to verify:
   ```bash
   python run_all_examples.py
   ```

3. Run a specific example:
   ```bash
   python examples/06_analytical/05_moving_average.py
   ```
