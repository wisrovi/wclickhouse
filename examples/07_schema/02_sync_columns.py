from pydantic import BaseModel

from wclickhouse import WClickHouse, get_client


class OldUser(BaseModel):
    __tablename__ = "sync_user"
    id: int
    username: str


class NewUser(BaseModel):
    __tablename__ = "sync_user"
    id: int
    username: str
    email: str = "default@example.com"


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 1. Start with old version
    print("--- Creating initial schema ---")
    WClickHouse(OldUser, db_config)

    # 2. Add new fields via NewUser model
    print("--- Syncing with new model (adding 'email' column) ---")
    db_new = WClickHouse(NewUser, db_config)

    # Verify columns
    client = get_client(db_config)
    columns = client.query(f"DESCRIBE TABLE {db_new.table_name}")
    print("Current columns:")
    for row in columns.result_rows:
        print(f" - {row[0]}: {row[1]}")


if __name__ == "__main__":
    main()
