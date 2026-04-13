from pydantic import BaseModel

from wclickhouse import QueryBuilder, WClickHouse


class Sale(BaseModel):
    sale_id: int
    amount: float
    region: str
    year: int


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Sale, db_config)

    # 1. Complex WHERE clauses with QueryBuilder
    builder = QueryBuilder("sale")
    builder.select("*").where("region = %(reg)s", reg="Europe").where(
        "amount >= %(min_amt)s", min_amt=500.0
    ).where("year IN %(years)s", years=[2023, 2024]).order_by(
        "amount", desc=True
    ).limit(
        10
    )

    sql, params = builder.build()
    print(f"Generated SQL: {sql}")
    print(f"Parameters: {params}")

    # 2. Execute query
    results = db.query(sql, parameters=params)
    print(f"Retrieved {len(results)} sales records.")


if __name__ == "__main__":
    main()
