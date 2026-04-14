import pytest
import decimal
from enum import Enum
from unittest.mock import MagicMock, patch
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from wclickhouse import WClickHouse
from wclickhouse.utils.types import get_clickhouse_type

class EdgeModel(BaseModel):
    __tablename__ = "test_edge_cases"
    id: int
    price: decimal.Decimal = Field(default=decimal.Decimal("10.00"))
    metadata: Dict[str, str] = Field(default_factory=dict)

@pytest.fixture
def db_config():
    return {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

def test_type_mapping_branches():
    """Cover remaining branches in types.py."""
    class DummyEnum(Enum):
        A = "a"
    
    class ModelWithComplex(BaseModel):
        e: DummyEnum
        m: Dict[str, int]
        d: decimal.Decimal
        opt_list: Optional[List[str]] = None
        
    fields = ModelWithComplex.model_fields
    assert "String" == get_clickhouse_type(fields['e'])
    assert "Map(String, Int64)" == get_clickhouse_type(fields['m'])
    assert "Decimal(18, 4)" == get_clickhouse_type(fields['d'])
    assert "Nullable(Array(String))" == get_clickhouse_type(fields['opt_list'])

def test_repository_edge_cases(db_config):
    """Cover error handling and special methods in repository.py."""
    db = WClickHouse(EdgeModel, db_config)
    
    # 1. Ping success
    assert db.ping() is True
    
    # 2. Empty inserts
    db.insert_many([])
    
    # 3. get_by_field empty
    db.get_by_field()
    
    # 4. update/delete no updates
    db.update("id=1")
    
    # 5. Buffer logic
    db_buf = WClickHouse(EdgeModel, db_config, use_buffer=True, buffer_size=2)
    db_buf.insert(EdgeModel(id=1))
    db_buf.insert_many([EdgeModel(id=2), EdgeModel(id=3)]) # Triggers flush
    assert db_buf.count() >= 2
    del db_buf

@patch("wclickhouse.core.repository.get_client")
def test_ping_failure(mock_get_client, db_config):
    """Cover Exception branch in ping."""
    mock_get_client.side_effect = Exception("Connection lost")
    db = MagicMock(spec=WClickHouse)
    db.db_config = db_config
    # Manually calling the real ping method on a mock/instance
    result = WClickHouse.ping(db)
    assert result is False

def test_arrow_import_error(monkeypatch):
    """Cover the ImportError branches when pa is not present."""
    import wclickhouse.core.repository as repo
    monkeypatch.setattr(repo, "HAS_ARROW", False)
    
    # Use a dummy instance
    db = MagicMock(spec=WClickHouse)
    
    with pytest.raises(ImportError, match="pyarrow is required"):
        repo.WClickHouse.insert_arrow(db, None)
    
    with pytest.raises(ImportError, match="pyarrow is required"):
        repo.WClickHouse.query_arrow(db, "SELECT 1")
