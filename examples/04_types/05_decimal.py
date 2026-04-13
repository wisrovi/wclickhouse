from decimal import Decimal
from pydantic import BaseModel
from wclickhouse import WClickHouse

# 1. Define your model with Decimal fields
class Transaction(BaseModel):
    transaction_id: int
    # Maps to Decimal(18, 4) in ClickHouse by default via our updated type mapper
    amount: Decimal
    tax: Decimal

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # 2. Initialize repository
    db = WClickHouse(Transaction, db_config)

    # 3. Create records with high precision decimals
    txs = [
        Transaction(transaction_id=1, amount=Decimal("1234.5678"), tax=Decimal("0.1500")),
        Transaction(transaction_id=2, amount=Decimal("99.99"), tax=Decimal("0.08")),
    ]

    print("Inserting transactions with Decimal values...")
    db.insert_many(txs)

    # 4. Fetch and verify precision
    print("Fetching transactions...")
    all_txs = db.get_all()
    for tx in all_txs:
        print(f"ID: {tx.transaction_id}, Amount: {tx.amount}, Tax: {tx.tax} (type: {type(tx.amount)})")

    print("\nDone!")

if __name__ == "__main__":
    main()
