from pydantic import BaseModel

from wclickhouse import QueryBuilder, WClickHouse


class DuplicateUser(BaseModel):
    __tablename__ = "replacing_user"
    id: int
    name: str
    version: int


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 1. Using ReplacingMergeTree for automatic de-duplication
    # 'version' column is used for deciding which version is newer
    print("--- Using ReplacingMergeTree ---")
    engine = "ReplacingMergeTree(version) ORDER BY id"
    db = WClickHouse(DuplicateUser, db_config, engine=engine)

    # 2. Insert duplicates
    db.insert_many(
        [
            DuplicateUser(id=1, name="Alice v1", version=1),
            DuplicateUser(id=1, name="Alice v2", version=2),
        ]
    )

    # 3. Query without FINAL (might show both)
    print("--- Normal Query ---")
    normal_results = db.get_all()
    print(f"Results without FINAL: {len(normal_results)}")

    # 4. Query with FINAL modifier using QueryBuilder
    print("--- Query with FINAL ---")
    query, params = QueryBuilder("replacing_user").final().build()
    final_results = db.query(query, params)
    print(f"Results with FINAL: {len(final_results)}")
    if final_results:
        print(f"Latest name: {final_results[0].name}")


if __name__ == "__main__":
    main()
