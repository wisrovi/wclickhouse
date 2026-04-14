import time
from pydantic import BaseModel
from wclickhouse import WClickHouse


class LogEntry(BaseModel):
    __tablename__ = "buffer_logs"
    id: int
    message: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 1. Initialize with Buffer Manager enabled
    # buffer_size=100 means it will only hit the DB every 100 inserts
    print("--- Initializing Buffer Manager (size=100) ---")
    db = WClickHouse(LogEntry, db_config, use_buffer=True, buffer_size=100)
    db.delete_all()

    # 2. Perform many small inserts
    print("Inserting 250 records one by one...")
    start_time = time.perf_counter()
    
    for i in range(250):
        db.insert(LogEntry(id=i, message=f"Log message {i}"))
        if (i + 1) % 50 == 0:
            current_count = db.count() # This will only show flushed records
            print(f"  > After {i+1} inserts, DB count is: {current_count}")

    # 3. Final flush
    print("Finalizing remaining records in buffer...")
    db.flush()
    
    final_count = db.count()
    duration = time.perf_counter() - start_time
    print(f"--- Finished ---")
    print(f"Total records in DB: {final_count}")
    print(f"Duration: {duration:.4f}s")


if __name__ == "__main__":
    main()
