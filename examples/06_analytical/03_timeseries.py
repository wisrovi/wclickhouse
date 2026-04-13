from datetime import datetime, timedelta

from pydantic import BaseModel

from wclickhouse import WClickHouse, get_client


class Measurement(BaseModel):
    sensor_id: str
    temperature: float
    timestamp: datetime


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }
    db = WClickHouse(Measurement, db_config)

    # Insert time-series data
    now = datetime.now()
    db.insert_many(
        [
            Measurement(
                sensor_id="A1", temperature=22.5, timestamp=now - timedelta(minutes=10)
            ),
            Measurement(
                sensor_id="A1", temperature=23.1, timestamp=now - timedelta(minutes=5)
            ),
            Measurement(sensor_id="A1", temperature=22.8, timestamp=now),
        ]
    )

    # Time-series analysis: Average by minute
    print("--- Time-Series Analysis ---")
    query = """
    SELECT
        toStartOfMinute(timestamp) as minute,
        avg(temperature) as avg_temp
    FROM measurement
    GROUP BY minute
    ORDER BY minute ASC
    """

    client = get_client(db_config)
    result = client.query(query)
    for row in result.result_rows:
        print(f"Time: {row[0]}, Avg Temp: {row[1]:.2f}")


if __name__ == "__main__":
    main()
