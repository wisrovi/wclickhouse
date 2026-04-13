from pydantic import BaseModel

from wclickhouse import WClickHouse, get_client


class InitialTable(BaseModel):
    id: int
    name: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 1. First instantiation will create the table automatically
    print("--- Creating table automatically ---")
    db = WClickHouse(InitialTable, db_config)

    # Verify table existence
    client = get_client(db_config)
    exists = client.command(f"EXISTS TABLE {db.table_name}")
    print(f"Table '{db.table_name}' exists: {bool(exists)}")


if __name__ == "__main__":
    main()
