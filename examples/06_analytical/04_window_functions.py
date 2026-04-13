import asyncio
from datetime import datetime

from pydantic import BaseModel

from wclickhouse import WClickHouse


class Sales(BaseModel):
    sale_id: int
    category: str
    amount: float
    sale_date: datetime = datetime.now()


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Sales, db_config)

    print("--- Inserting sales data ---")
    sales_data = [
        Sales(sale_id=1, category="A", amount=100.0),
        Sales(sale_id=2, category="A", amount=200.0),
        Sales(sale_id=3, category="B", amount=150.0),
        Sales(sale_id=4, category="B", amount=50.0),
        Sales(sale_id=5, category="A", amount=300.0),
    ]
    db.insert_many(sales_data)

    print("--- Using ROW_NUMBER() OVER(PARTITION BY category ORDER BY amount DESC) ---")
    # ClickHouse supports window functions since version 21.3
    query = """
    SELECT 
        sale_id, 
        category, 
        amount, 
        ROW_NUMBER() OVER(PARTITION BY category ORDER BY amount DESC) as rank
    FROM sales
    ORDER BY category, rank
    """
    
    from wclickhouse import get_client
    client = get_client(db_config)
    result = client.query(query)
    
    for row in result.named_results():
        print(f"ID: {row['sale_id']}, Category: {row['category']}, Amount: {row['amount']}, Rank: {row['rank']}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
