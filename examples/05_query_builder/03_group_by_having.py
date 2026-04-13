from pydantic import BaseModel

from wclickhouse import QueryBuilder, WClickHouse


class Sale(BaseModel):
    sale_id: int
    amount: float
    region: str
    category: str


# Model for the aggregation result
class SalesByRegion(BaseModel):
    region: str
    total_amount: float
    avg_amount: float


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # Initialize with the base model to ensure table exists
    WClickHouse(Sale, db_config)

    # 1. Group By and Having with QueryBuilder
    builder = QueryBuilder("sale")
    builder.select(
        "region", "sum(amount) as total_amount", "avg(amount) as avg_amount"
    ).group_by("region").having("total_amount > 1000.0")

    sql, params = builder.build()
    print(f"Generated SQL: {sql}")

    # 2. To get the results as SalesByRegion models, we can use a temporary WClickHouse repo
    # or use the underlying client directly.
    # Here we use the repo with the results model:
    WClickHouse(SalesByRegion, db_config)

    # Note: SalesByRegion won't create a table if it matches an existing one
    # but here it's just used to map the query results.
    # Actually, WClickHouse(SalesByRegion) WOULD try to create a table 'salesbyregion'.
    # A better way is to use db.query with a different model if allowed,
    # but db.query uses self.model.

    # Let's check if WClickHouse allows passing a custom model to query...
    # It doesn't. It uses self.model.

    # Correct way using the library:
    # We can create a repository for the results model (pointing to the same or no table)
    # or just use the current one and handle the results if they were compatible.

    # Alternative: use the internal client
    from wclickhouse import get_client

    client = get_client(db_config)
    result = client.query(sql)

    print("Aggregation Results:")
    for row in result.result_rows:
        data = dict(zip(result.column_names, row))
        report = SalesByRegion(**data)
        print(
            f" - {report.region}: Total={report.total_amount}, Avg={report.avg_amount:.2f}"
        )


if __name__ == "__main__":
    main()
