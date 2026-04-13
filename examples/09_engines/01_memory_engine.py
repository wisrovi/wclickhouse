from pydantic import BaseModel

from wclickhouse import WClickHouse


class TempData(BaseModel):
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

    # 1. Using Memory() engine for high speed, transient data
    print("--- Using Memory() Engine ---")
    db = WClickHouse(TempData, db_config, engine="Memory()")

    db.insert(TempData(id=1, data="fast data"))
    all_data = db.get_all()
    print(f"Items in Memory: {len(all_data)}")


if __name__ == "__main__":
    main()
