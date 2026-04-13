import asyncio
import os
import sys
import time
import pandas as pd
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Add src to path
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

from wclickhouse import WClickHouse, get_client

# DB Configuration (Match docker-compose)
DB_CONFIG = {
    "host": "localhost",
    "port": 8124,
    "username": "default",
    "password": "test_pass",
    "database": "default",
}

# Massive Load Config
TOTAL_RECORDS = 100_000  # 100k for a quick but significant test
BATCH_SIZE = 10_000      # Optimized batch size for ClickHouse

class HeavyModel(BaseModel):
    __tablename__ = "stress_test_heavy"
    event_id: int
    user_id: str
    action: str
    value: float
    tags: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

def run_benchmark():
    print("="*60)
    print("wclickhouse MASSIVE STRESS & BENCHMARK")
    print("="*60)
    
    db = WClickHouse(HeavyModel, DB_CONFIG)
    db.delete_all() # Clean start
    
    # 1. Row-by-row Insert (The "Wrong" Way - To show why rivals fail if they don't bulk)
    print(f"\n[1/4] Testing Row-by-Row insertion ({1000} records)...")
    start = time.perf_counter()
    for i in range(1000):
        db.insert(HeavyModel(event_id=i, user_id=f"user_{i}", action="click", value=i*1.1, tags=["stress", "test"]))
    duration = time.perf_counter() - start
    print(f"  -> Duration: {duration:.2f}s ({1000/duration:.2f} rec/s)")

    # 2. Bulk Insert with Pydantic (The "Wisrovi" Way)
    print(f"\n[2/4] Testing Bulk Insertion with Pydantic ({TOTAL_RECORDS:,} records)...")
    records = [
        HeavyModel(event_id=i, user_id=f"user_{i}", action="view", value=i*0.5, tags=["bulk", "pydantic"])
        for i in range(TOTAL_RECORDS)
    ]
    
    start = time.perf_counter()
    for i in range(0, TOTAL_RECORDS, BATCH_SIZE):
        batch = records[i:i+BATCH_SIZE]
        db.insert_many(batch)
    duration = time.perf_counter() - start
    print(f"  -> Duration: {duration:.2f}s ({TOTAL_RECORDS/duration:.2f} rec/s)")

    # 3. Dataframe Insert (The "Analytical" Way)
    print(f"\n[3/4] Testing DataFrame Insertion ({TOTAL_RECORDS:,} records)...")
    df = pd.DataFrame([
        {"event_id": i, "user_id": f"user_{i}", "action": "scroll", "value": i*0.2, "tags": ["pandas", "fast"], "timestamp": datetime.now()}
        for i in range(TOTAL_RECORDS)
    ])
    
    start = time.perf_counter()
    db.insert_dataframe(df)
    duration = time.perf_counter() - start
    print(f"  -> Duration: {duration:.2f}s ({TOTAL_RECORDS/duration:.2f} rec/s)")

    # 4. Complex Analytical Query
    print(f"\n[4/4] Testing Heavy Analytical Query...")
    start = time.perf_counter()
    query = """
    SELECT 
        action, 
        avg(value) as avg_val, 
        count() as total,
        length(tags) as tags_len
    FROM stress_test_heavy 
    GROUP BY action, tags_len
    ORDER BY total DESC
    """
    # Use the raw client to get results that don't match the model
    client = get_client(DB_CONFIG)
    result = client.query(query)
    duration = time.perf_counter() - start
    print(f"  -> Query Duration: {duration:.4f}s")
    print(f"  -> Results rows: {len(result.result_rows)}")
    for row in result.result_rows[:3]:
        print(f"     Row: {row}")
    
    print("\n" + "="*60)
    print("STRESS TEST COMPLETED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    try:
        run_benchmark()
    except Exception as e:
        print(f"STRESS TEST FAILED: {e}")
        sys.exit(1)
