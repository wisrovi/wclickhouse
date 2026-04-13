from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from wclickhouse import WClickHouse, get_async_client


# 1. Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 8124,
    "username": "default",
    "password": "test_pass",
    "database": "default",
}


# 2. Data Model
class Item(BaseModel):
    id: int
    name: str
    price: float


# 3. FastAPI Lifespan (Optional but recommended for global cleanup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize connection or run migrations here if needed
    yield
    # Cleanup: close_global_clients() could be used here if needed


app = FastAPI(lifespan=lifespan)


# 4. Dependency Injection Pattern
async def get_db() -> AsyncGenerator[WClickHouse, None]:
    # We use the specific model for this "repository"
    db = WClickHouse(Item, DB_CONFIG)
    yield db


# 5. FastAPI Endpoints
@app.post("/items/")
async def create_item(item: Item, db: WClickHouse = Depends(get_db)):
    await db.insert_async(item)
    return {"status": "item created", "id": item.id}


@app.get("/items/count")
async def get_items_count(db: WClickHouse = Depends(get_db)):
    count = await db.count_async()
    return {"total": count}


@app.get("/items/native-client")
async def use_native_client():
    # Example using the low-level client if needed
    client = await get_async_client(DB_CONFIG)
    result = await client.query("SELECT version()")
    return {"clickhouse_version": result.first_item["version()"]}


if __name__ == "__main__":
    print("Run this example using: uvicorn 01_fastapi_async:app --reload")
    print("--- Example setup complete ---")
    # To run this code directly in the terminal (mocking a request)
    import asyncio
    async def test_run():
        db = WClickHouse(Item, DB_CONFIG)
        await db.insert_async(Item(id=99, name="FastAPI test", price=12.5))
        c = await db.count_async()
        print(f"Total items: {c}")

    try:
        asyncio.run(test_run())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ClickHouse is running (use docker-compose up -d)")
