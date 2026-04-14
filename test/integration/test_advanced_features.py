import pytest
import asyncio
import pyarrow as pa
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from wclickhouse import WClickHouse, close_global_clients

class Color(str, Enum):
    RED = "red"
    BLUE = "blue"

class AdvancedModel(BaseModel):
    __tablename__ = "test_advanced_features"
    id: int
    color: Color
    tags: List[str]
    category: str = Field(json_schema_extra={"clickhouse_type": "LowCardinality(String)"})

@pytest.fixture
def db_config():
    return {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

def test_buffer_manager(db_config):
    """Test the Buffer Manager logic."""
    db = WClickHouse(AdvancedModel, db_config, use_buffer=True, buffer_size=10)
    db.delete_all()
    
    # 1. Fill partial buffer
    for i in range(5):
        db.insert(AdvancedModel(id=i, color=Color.RED, tags=[], category="test"))
    
    assert db.count() == 0  # Still in buffer
    
    # 2. Trigger auto-flush
    for i in range(5, 10):
        db.insert(AdvancedModel(id=i, color=Color.BLUE, tags=[], category="test"))
    
    assert db.count() == 10  # Auto-flushed at 10
    
    # 3. Manual flush
    db.insert(AdvancedModel(id=100, color=Color.RED, tags=[], category="test"))
    assert db.count() == 10
    db.flush()
    assert db.count() == 11

def test_apache_arrow_integration(db_config):
    """Test insert_arrow and query_arrow with simpler types."""
    db = WClickHouse(AdvancedModel, db_config)
    db.delete_all()
    
    # 1. Insert via Arrow
    data = {
        "id": [1, 2],
        "color": ["red", "blue"],
        "tags": [["t1"], []],
        "category": ["cat1", "cat1"]
    }
    table = pa.Table.from_pydict(data)
    db.insert_arrow(table)
    
    assert db.count() == 2
    
    # 2. Query via Arrow
    res_table = db.query_arrow(f"SELECT * FROM {db.table_name}")
    assert isinstance(res_table, pa.Table)
    assert res_table.num_rows == 2

def test_query_streaming(db_config):
    """Test the lazy loading query_stream."""
    db = WClickHouse(AdvancedModel, db_config)
    db.delete_all()
    
    items = [AdvancedModel(id=i, color=Color.RED, tags=[], category="s") for i in range(20)]
    db.insert_many(items)
    
    stream_count = 0
    for item in db.query_stream(f"SELECT * FROM {db.table_name}"):
        assert isinstance(item, AdvancedModel)
        stream_count += 1
    
    assert stream_count == 20

@pytest.mark.asyncio
async def test_async_advanced_features(db_config):
    """Test async versions of new features."""
    db = WClickHouse(AdvancedModel, db_config, use_buffer=True, buffer_size=5)
    
    # Async buffer flush
    await db.insert_async(AdvancedModel(id=99, color=Color.RED, tags=[], category="a"))
    await db.flush_async()
    
    # Async Arrow query
    res = await db.query_arrow_async(f"SELECT count() FROM {db.table_name}")
    assert res.num_rows == 1
    
    # Cleanup
    db.delete_all()

def test_global_cleanup():
    """Cover close_global_clients."""
    close_global_clients()
