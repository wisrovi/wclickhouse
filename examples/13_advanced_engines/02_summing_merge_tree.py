from pydantic import BaseModel
from wclickhouse import WClickHouse


class SalesSummary(BaseModel):
    __tablename__ = "sales_summary"
    date: str
    product_id: int
    quantity: int
    revenue: float


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 1. Use SummingMergeTree to automatically aggregate rows with the same primary key
    # ClickHouse will sum the 'quantity' and 'revenue' columns on merge
    engine = "SummingMergeTree() ORDER BY (date, product_id)"
    db = WClickHouse(SalesSummary, db_config, engine=engine)

    # 2. Insert duplicate keys
    db.insert_many([
        SalesSummary(date="2026-04-13", product_id=1, quantity=10, revenue=100.0),
        SalesSummary(date="2026-04-13", product_id=1, quantity=5, revenue=50.0),
    ])

    # 3. Query (ClickHouse sums values automatically)
    # Note: Merges are background tasks, so we might still see 2 rows unless we use SUM in query
    print("--- SummingMergeTree Results ---")
    query = "SELECT date, product_id, sum(quantity), sum(revenue) FROM sales_summary GROUP BY date, product_id"
    from wclickhouse import get_client
    client = get_client(db_config)
    result = client.query(query)
    for row in result.result_rows:
        print(f"Date: {row[0]}, ID: {row[1]}, Total Qty: {row[2]}, Total Rev: {row[3]}")


if __name__ == "__main__":
    main()
