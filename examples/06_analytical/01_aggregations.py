import asyncio

from pydantic import BaseModel

from wclickhouse import WClickHouse


class Metric(BaseModel):
    metric_name: str
    value: float


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }
    db = WClickHouse(Metric, db_config)

    # Insert some data
    db.insert_many(
        [
            Metric(metric_name="cpu", value=10.5),
            Metric(metric_name="cpu", value=15.2),
            Metric(metric_name="mem", value=20.1),
        ]
    )

    # Aggregation using raw SQL query
    print("--- Aggregations ---")
    query = "SELECT metric_name, sum(value) as total, avg(value) as mean FROM metric GROUP BY metric_name"
    # Note: query returns list of Pydantic models, but if fields don't match exactly,
    # it might need a temporary model or raw client access.
    # For simplicity, we use the client directly for custom aggregations if they don't map to 'Metric'
    from wclickhouse import get_client

    c = get_client(db_config)
    result = c.query(query)
    for row in result.result_rows:
        print(f"Name: {row[0]}, Sum: {row[1]}, Avg: {row[2]}")


if __name__ == "__main__":
    asyncio.run(main())
