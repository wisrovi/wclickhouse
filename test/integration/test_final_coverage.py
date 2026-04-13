import pytest
import asyncio
from pydantic import BaseModel
from wclickhouse import WClickHouse

class SyncModel(BaseModel):
    __tablename__ = "test_sync_final"
    id: int

@pytest.fixture
def db_config():
    return {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

@pytest.mark.asyncio
async def test_extra_coverage(db_config):
    """Cover the last remaining lines in sync and repository."""
    db = WClickHouse(SyncModel, db_config)
    
    # Coverage for sync_with_model_async and create_if_not_exists_async
    await db._sync.create_if_not_exists_async()
    await db._sync.sync_with_model_async()
    
    # Coverage for specific repository methods
    # delete_all
    db.insert(SyncModel(id=1))
    db.delete_all()
    assert db.count() == 0
    
    # insert_async with one record
    await db.insert_async(SyncModel(id=100))
    assert await db.count_async() == 1
    
    # update and delete (asynchronous mutations)
    db.update("id = 100", id=200)
    db.delete("id = 200")
    
    # Async version of update and delete
    await db.update_async("id = 1", id=2)
    await db.delete_async("id = 2")
    
    # Final cleanup
    db.delete_all()

def test_sync_new_fields(db_config):
    """Cover the branch where new fields are added to an existing table."""
    class Base(BaseModel):
        __tablename__ = "sync_fields_test"
        id: int
        
    db1 = WClickHouse(Base, db_config)
    db1.delete_all()
    
    class Extended(BaseModel):
        __tablename__ = "sync_fields_test"
        id: int
        name: str
        tags: list[str]
        
    # This should trigger the new_fields branch in sync_with_model
    db2 = WClickHouse(Extended, db_config)
    cols = db2._sync.get_columns()
    assert "name" in cols
    assert "tags" in cols
