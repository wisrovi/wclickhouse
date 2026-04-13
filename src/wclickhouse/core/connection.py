"""Connection management for ClickHouse using clickhouse-connect."""

import asyncio
import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Optional

import clickhouse_connect
from clickhouse_connect.driver.client import Client

logger = logging.getLogger(__name__)

# Global clients to reuse connections (HTTP keep-alive)
_global_clients: dict[str, Client] = {}


def _get_client_key(db_config: dict[str, Any]) -> str:
    """Generate a unique key for the client based on config."""
    return f"{db_config.get('host', 'localhost')}:{db_config.get('port', 8124)}:{db_config.get('database', 'default')}:{db_config.get('username', 'default')}"


def get_client(db_config: dict[str, Any]) -> Client:
    """Get or create a ClickHouse client (sync).

    Args:
        db_config: Database configuration dictionary.

    Returns:
        Client: A clickhouse-connect client instance.
    """
    key = _get_client_key(db_config)
    if key not in _global_clients:
        # clickhouse-connect handles its own connection pooling/keep-alive internally
        _global_clients[key] = clickhouse_connect.get_client(**db_config)
        logger.info("Created new ClickHouse client for %s", key)
    return _global_clients[key]


async def get_async_client(db_config: dict[str, Any]) -> Client:
    """Get a ClickHouse client for async use.

    Wraps the sync client retrieval in a thread to avoid blocking.

    Args:
        db_config: Database configuration dictionary.

    Returns:
        Client: A clickhouse-connect client instance.
    """
    return await asyncio.to_thread(get_client, db_config)


class ClickHouseConnection:
    """Context manager for ClickHouse operations (sync).

    ClickHouse doesn't support standard ACID transactions for most engines,
    but this provides a familiar interface.
    """

    def __init__(self, db_config: dict[str, Any]):
        self.db_config = db_config
        self.client: Optional[Client] = None

    def __enter__(self) -> Client:
        self.client = get_client(self.db_config)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # No commit/rollback needed for ClickHouse standard engines
        pass


class AsyncClickHouseConnection:
    """Async context manager for ClickHouse operations."""

    def __init__(self, db_config: dict[str, Any]):
        self.db_config = db_config
        self.client: Optional[Client] = None

    async def __aenter__(self) -> Client:
        self.client = await get_async_client(self.db_config)
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


@contextmanager
def get_connection(db_config: dict[str, Any]) -> Generator[Client, None, None]:
    """Get a ClickHouse connection context (sync)."""
    with ClickHouseConnection(db_config) as client:
        yield client


async def get_async_connection(db_config: dict[str, Any]):
    """Get a ClickHouse connection context (async)."""
    async with AsyncClickHouseConnection(db_config) as client:
        yield client


def close_global_clients():
    """Close all global ClickHouse clients."""
    global _global_clients
    for client in _global_clients.values():
        try:
            client.close()
        except Exception as e:
            logger.error("Error closing ClickHouse client: %s", e)
    _global_clients = {}
