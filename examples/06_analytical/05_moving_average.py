import asyncio
from datetime import datetime, timedelta

from pydantic import BaseModel

from wclickhouse import WClickHouse


class StockPrice(BaseModel):
    symbol: str
    price: float
    time: datetime


async def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(StockPrice, db_config)

    print("--- Inserting price data ---")
    now = datetime.now()
    price_data = [
        StockPrice(symbol="WSC", price=100.0 + i * 2, time=now - timedelta(days=10-i))
        for i in range(10)
    ]
    db.insert_many(price_data)

    print("--- Using moving average (avg OVER ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) ---")
    query = """
    SELECT 
        time, 
        price, 
        avg(price) OVER (ORDER BY time ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
    FROM stock_price
    ORDER BY time
    """
    
    from wclickhouse import get_client
    client = get_client(db_config)
    result = client.query(query)
    
    for row in result.named_results():
        print(f"Time: {row['time']}, Price: {row['price']:.2f}, Moving Avg (3-day): {row['moving_avg']:.2f}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
