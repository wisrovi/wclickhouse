from pydantic import BaseModel

from wclickhouse import WClickHouse


class User(BaseModel):
    id: int


def main():
    # Example: Invalid host configuration
    wrong_config = {
        "host": "non_existent_server",
        "port": 8124,
    }

    print("--- Testing Connectivity Handling ---")
    try:
        # Note: Initialization will try to sync schema and might fail if server is down
        WClickHouse(User, wrong_config)
    except Exception as e:
        print(f"Caught expected error: {e}")


if __name__ == "__main__":
    main()
