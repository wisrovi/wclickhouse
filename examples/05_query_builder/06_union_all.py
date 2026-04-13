from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define common model
class LogEntry(BaseModel):
    timestamp: int
    message: str
    source: str

# 2. Define specific models for different tables
class SystemLog(LogEntry):
    __tablename__ = "system_log"

class AppLog(LogEntry):
    __tablename__ = "app_log"

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 3. Initialize repositories and create sample data
    sys_db = WClickHouse(SystemLog, db_config)
    app_db = WClickHouse(AppLog, db_config)

    sys_db.delete_all()
    app_db.delete_all()

    sys_db.insert_many([
        SystemLog(timestamp=1000, message="Kernel boot", source="kernel"),
        SystemLog(timestamp=1001, message="CPU online", source="kernel"),
    ])

    app_db.insert_many([
        AppLog(timestamp=2000, message="App started", source="app_main"),
        AppLog(timestamp=2001, message="DB connected", source="app_db"),
    ])

    # 4. Perform UNION ALL using raw SQL
    # We can use any of the DB instances as long as the model matches the result schema
    sql = f"""
    SELECT timestamp, message, source FROM system_log
    UNION ALL
    SELECT timestamp, message, source FROM app_log
    ORDER BY timestamp ASC
    """

    print("Executing UNION ALL query...")
    results = sys_db.query(sql)

    # 5. Process combined results
    for log in results:
        print(f"[{log.timestamp}] {log.source}: {log.message}")

    print("\nDone!")

if __name__ == "__main__":
    main()
