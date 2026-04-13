from pydantic import BaseModel

from wclickhouse import QueryBuilder, WClickHouse


class Product(BaseModel):
    product_id: int
    name: str
    price: float
    category: str


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Product, db_config)

    # 1. Simple select using QueryBuilder
    builder = QueryBuilder("product")
    builder.select("name", "price").where("price > 10.0").limit(5)

    sql, params = builder.build()
    print(f"Generated SQL: {sql}")

    # 2. Execute query
    # Note: query() returns full model instances, so non-selected fields will be defaulted
    # or should be included if model validation requires them.
    # For partial results, it's better to use another model or the client directly.
    # Here we select all fields to match the model.
    builder = (
        QueryBuilder("product")
        .select("*")
        .where("category = %(cat)s", cat="Electronics")
    )
    sql, params = builder.build()

    results = db.query(sql, parameters=params)
    print(f"Found {len(results)} electronic products.")


if __name__ == "__main__":
    main()
