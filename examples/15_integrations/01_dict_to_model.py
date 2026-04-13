from typing import List
from pydantic import BaseModel, TypeAdapter
from wclickhouse import WClickHouse

class LegacyData(BaseModel):
    id: int
    raw_info: str

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    # Imagine this comes from a legacy system or a JSON file
    external_list = [
        {"id": 1, "raw_info": "First item"},
        {"id": 2, "raw_info": "Second item"},
        {"id": 3, "raw_info": "Third item"},
    ]

    # 1. Efficiently convert list of dicts to list of Pydantic models
    # This is useful when you have a lot of data from a non-Pydantic source
    print("--- Converting Dict List to Models ---")
    adapter = TypeAdapter(List[LegacyData])
    models = adapter.validate_python(external_list)
    
    print(f"Successfully validated {len(models)} models.")

    # 2. Insert into ClickHouse
    db = WClickHouse(LegacyData, db_config)
    db.delete_all()
    db.insert_many(models)
    
    print(f"Inserted {db.count()} records.")

if __name__ == "__main__":
    main()
