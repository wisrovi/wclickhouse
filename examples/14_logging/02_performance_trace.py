import time
from functools import wraps
from pydantic import BaseModel
from wclickhouse import WClickHouse, get_client

def trace_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"DEBUG: Execution of {func.__name__} took {duration:.4f} seconds")
        return result
    return wrapper

class TraceModel(BaseModel):
    __tablename__ = "tracemodel"
    id: int
    data: str

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(TraceModel, db_config)

    # 1. Trace insertion performance
    print("--- Tracing Insertion ---")
    @trace_performance
    def bulk_insert():
        batch = [TraceModel(id=i, data=f"data_{i}") for i in range(5000)]
        db.insert_many(batch)
    
    bulk_insert()

    # 2. Trace query performance
    print("\n--- Tracing Query ---")
    @trace_performance
    def run_complex_query():
        # Use direct client for aggregations to avoid Pydantic validation errors
        client = get_client(db_config)
        return client.query("SELECT count(), max(id) FROM tracemodel")
    
    result = run_complex_query()
    print(f"Result: {result.result_rows[0]}")

if __name__ == "__main__":
    main()
