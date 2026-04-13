from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from wclickhouse import WClickHouse, close_global_clients


@pytest.fixture(autouse=True)
def cleanup_clients():
    """Clear global clients before and after each test."""
    close_global_clients()
    yield
    close_global_clients()


class User(BaseModel):
    user_id: int
    username: str
    is_active: bool


@pytest.fixture
def mock_db_config():
    return {
        "host": "localhost",
        "port": 8124,
        "database": "default",
    }


def test_initialization(mock_db_config):
    """Test that initialization calls sync methods."""
    with patch("wclickhouse.core.repository.TableSync") as MockSync:
        db = WClickHouse(User, mock_db_config)

        # Verify sync methods were called
        MockSync.return_value.create_if_not_exists.assert_called_once()
        MockSync.return_value.sync_with_model.assert_called_once()
        assert db.table_name == "user"


@patch("wclickhouse.core.connection.clickhouse_connect.get_client")
@patch("wclickhouse.core.repository.TableSync")
def test_insert_many(MockSync, mock_clickhouse_get_client, mock_db_config):
    """Test insert_many maps data correctly to client.insert."""
    mock_client = MagicMock()
    mock_clickhouse_get_client.return_value = mock_client

    db = WClickHouse(User, mock_db_config)

    users = [
        User(user_id=1, username="alice", is_active=True),
        User(user_id=2, username="bob", is_active=False),
    ]

    db.insert_many(users)

    # Check that client.insert was called with correct arguments
    mock_client.insert.assert_called_once()
    args, kwargs = mock_client.insert.call_args
    assert args[0] == "user"
    assert len(args[1]) == 2
    assert args[1][0] == [1, "alice", True]
    assert kwargs["column_names"] == ["user_id", "username", "is_active"]


@patch("wclickhouse.core.connection.clickhouse_connect.get_client")
@patch("wclickhouse.core.repository.TableSync")
def test_get_all(MockSync, mock_clickhouse_get_client, mock_db_config):
    """Test get_all maps results back to Pydantic models."""
    mock_client = MagicMock()
    mock_clickhouse_get_client.return_value = mock_client

    # Mock result from clickhouse-connect
    mock_result = MagicMock()
    mock_result.column_names = ["user_id", "username", "is_active"]
    mock_result.result_rows = [
        (1, "alice", True),
        (2, "bob", False),
    ]
    mock_client.query.return_value = mock_result

    db = WClickHouse(User, mock_db_config)
    users = db.get_all()

    assert len(users) == 2
    assert isinstance(users[0], User)
    assert users[0].username == "alice"
    assert users[1].username == "bob"
    assert users[1].is_active is False
