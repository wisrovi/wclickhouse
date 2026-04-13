import asyncio

from pydantic import BaseModel, Field

from wclickhouse import WClickHouse


class DailySales(BaseModel):
    # __tablename__ = "daily_sales"
    product: str = Field(..., json_schema_extra={"clickhouse_type": "String"})
    # SimpleAggregateFunction(sum, Int64) will automatically sum values on merge
    total_amount: int = Field(..., json_schema_extra={"clickhouse_type": "SimpleAggregateFunction(sum, Int64)"})


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # Define the engine for the table
    engine = "AggregatingMergeTree() ORDER BY product"
    
    db = WClickHouse(DailySales, db_config, engine=engine)

    print("--- Inserting partial sales for 'Laptop' ---")
    db.insert_many([
        DailySales(product="Laptop", total_amount=1000),
        DailySales(product="Laptop", total_amount=500),
    ])

    print("--- Querying results (using sum() to see the aggregated value) ---")
    # Even with AggregatingMergeTree, you should use aggregate functions in SELECT 
    # because merges happen asynchronously in the background.
    query = "SELECT product, sum(total_amount) as total FROM daily_sales GROUP BY product"
    
    from wclickhouse import get_client
    client = get_client(db_config)
    result = client.query(query)
    
    for row in result.named_results():
        print(f"Product: {row['product']}, Total Sales: {row['total']}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
