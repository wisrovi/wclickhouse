import pytest
import asyncio
from pydantic import BaseModel
from wclickhouse import WClickHouse, get_async_client, close_global_clients
from wclickhouse.core.connection import ClickHouseConnection, AsyncClickHouseConnection, get_connection, get_async_connection

class AsyncModel(BaseModel):
    __tablename__ = "test_async_coverage"
    id: int
    data: str

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
async def test_connection_managers(db_config):
    """Test connection managers (sync/async) and global clients."""
    # Test ClickHouseConnection
    with ClickHouseConnection(db_config) as client:
        assert client.command("SELECT 1") == 1
    
    # Test AsyncClickHouseConnection
    async with AsyncClickHouseConnection(db_config) as client:
        assert client.command("SELECT 1") == 1
        
    # Test get_connection generator
    from wclickhouse.core.connection import get_connection
    with get_connection(db_config) as client:
        assert client.command("SELECT 1") == 1
        
    # Test get_async_connection generator
    from wclickhouse.core.connection import get_async_connection
    async for client in get_async_connection(db_config):
        assert client.command("SELECT 1") == 1
        
    # Test get_async_client
    client = await get_async_client(db_config)
    assert client.command("SELECT 1") == 1
    
    # Test close_global_clients
    close_global_clients()

@pytest.mark.asyncio
async def test_async_sync_operations(db_config):
    """Test async operations in TableSync and Repository."""
    db = WClickHouse(AsyncModel, db_config)
    
    # Async TableSync coverage
    assert await db._sync.table_exists_async() is True
    cols = await db._sync.get_columns_async()
    assert "id" in cols
    
    # Async Repository coverage
    await db.insert_async(AsyncModel(id=1, data="a"))
    await db.insert_many_async([AsyncModel(id=2, data="b")])
    
    import pandas as pd
    df = pd.DataFrame([{"id": 3, "data": "c"}])
    await db.insert_dataframe_async(df)
    
    assert await db.count_async() == 3
    
    results = await db.get_by_field_async(data="a")
    assert len(results) == 1
    
    first = await db.get_first_async()
    assert first is not None
    
    await db.update_async("id = 1", data="updated")
    
    # Custom query async
    query_res = await db.query_async("SELECT * FROM test_async_coverage WHERE id = 2")
    assert len(query_res) == 1

    await db._sync.drop_table_async()
    assert await db._sync.table_exists_async() is False
