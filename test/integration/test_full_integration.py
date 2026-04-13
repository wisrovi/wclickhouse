import pytest
import asyncio
import pandas as pd
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from wclickhouse import WClickHouse, QueryBuilder, TableSync, get_client

class FullModel(BaseModel):
    __tablename__ = "test_full_integration"
    id: int
    name: str
    tags: List[str]
    score: Optional[float] = None
    created_at: datetime = datetime.now()

@pytest.fixture
def db_config():
    return {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

def test_query_builder():
    """Test all methods of QueryBuilder."""
    qb = QueryBuilder("my_table")
    sql, params = qb.select("id", "name").where("id = %(id)s", id=1).order_by("name", desc=True).limit(10, 5).build()
    assert "SELECT id, name FROM my_table WHERE id = %(id)s ORDER BY name DESC LIMIT 10 OFFSET 5" == sql
    assert params == {"id": 1}
    
    qb_group = QueryBuilder("stats").group_by("category").having("count() > 10").final()
    sql_group, _ = qb_group.build()
    assert "SELECT * FROM stats FINAL GROUP BY category HAVING count() > 10" == sql_group

def test_types_mapping():
    """Test the type mapping logic indirectly through TableSync."""
    from wclickhouse.utils.types import get_clickhouse_type
    from pydantic.fields import FieldInfo
    
    class TypeTest(BaseModel):
        a: int
        b: str
        c: List[int]
        d: Optional[float]
        e: datetime

    fields = TypeTest.model_fields
    assert get_clickhouse_type(fields['a']) == "Int64"
    assert get_clickhouse_type(fields['b']) == "String"
    assert get_clickhouse_type(fields['c']) == "Array(Int64)"
    assert get_clickhouse_type(fields['d']) == "Nullable(Float64)"
    assert get_clickhouse_type(fields['e']) == "DateTime64(3)"

def test_full_repository_flow(db_config):
    """Test the complete flow of the repository with a real ClickHouse instance."""
    db = WClickHouse(FullModel, db_config)
    db.delete_all()
    
    # 1. Insert Many
    models = [
        FullModel(id=1, name="test1", tags=["a", "b"], score=10.5),
        FullModel(id=2, name="test2", tags=["c"], score=None)
    ]
    db.insert_many(models)
    assert db.count() == 2
    
    # 2. Get By Field
    results = db.get_by_field(name="test1")
    assert len(results) == 1
    assert results[0].id == 1
    
    # 3. Dataframe
    df = pd.DataFrame([{"id": 3, "name": "df", "tags": [], "score": 0.0, "timestamp": datetime.now()}])
    # Note: Column names in DF must match model
    df.columns = ["id", "name", "tags", "score", "created_at"]
    db.insert_dataframe(df)
    assert db.count() == 3
    
    # 4. Mutations (Update/Delete)
    db.update("id = 1", name="updated")
    # Mutations are async in ClickHouse, we might need a small sleep if we want to check immediately
    # but for testing the SQL generation/execution it's fine.
    
    # 5. Ping
    assert db.ping() is True
    
    # 6. Query with QueryBuilder integration
    sql, params = QueryBuilder(db.table_name).where("id = %(id)s", id=2).build()
    queried = db.query(sql, params)
    assert len(queried) == 1
    assert queried[0].name == "test2"

@pytest.mark.asyncio
async def test_async_repository_flow(db_config):
    """Test async methods of the repository."""
    db = WClickHouse(FullModel, db_config)
    db.delete_all()
    
    await db.insert_async(FullModel(id=10, name="async", tags=[]))
    assert await db.count_async() == 1
    
    results = await db.get_all_async()
    assert len(results) == 1
    assert results[0].name == "async"
    
    await db.delete_async("id = 10")
    assert await db.ping_async() is True

def test_schema_sync(db_config):
    """Test automatic schema synchronization."""
    class Simple(BaseModel):
        __tablename__ = "sync_test"
        id: int
    
    db1 = WClickHouse(Simple, db_config)
    db1.delete_all()
    
    class SimpleExtended(BaseModel):
        __tablename__ = "sync_test"
        id: int
        new_col: str = "default"
        
    db2 = WClickHouse(SimpleExtended, db_config)
    cols = db2._sync.get_columns()
    assert "new_col" in cols
