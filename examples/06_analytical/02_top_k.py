from pydantic import BaseModel

from wclickhouse import WClickHouse, get_client


class Interaction(BaseModel):
    user_id: int
    action: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }
    db = WClickHouse(Interaction, db_config)

    # Insert data
    db.insert_many(
        [
            Interaction(user_id=1, action="view"),
            Interaction(user_id=2, action="view"),
            Interaction(user_id=1, action="click"),
            Interaction(user_id=3, action="view"),
        ]
    )

    # Get Top-K actions
    print("--- Top-K Actions ---")
    query = "SELECT action, count() as total FROM interaction GROUP BY action ORDER BY total DESC LIMIT 10"

    # We use get_client directly for non-BaseModel queries
    client = get_client(db_config)
    result = client.query(query)
    for row in result.result_rows:
        print(f"Action: {row[0]}, Count: {row[1]}")


if __name__ == "__main__":
    main()
