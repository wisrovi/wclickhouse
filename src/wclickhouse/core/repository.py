"""Main repository class for ClickHouse operations."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel

from wclickhouse.core.connection import get_client
from wclickhouse.core.sync import TableSync

logger = logging.getLogger(__name__)

try:
    import pyarrow as pa
    HAS_ARROW = True
except ImportError:
    HAS_ARROW = False


class WClickHouse:
    """ClickHouse repository using Pydantic models.

    Provides a simple interface for CRUD and analytical operations on ClickHouse,
    optimized for bulk inserts and Pydantic validation.
    """

    def __init__(
        self,
        model: Type[BaseModel],
        db_config: Dict[str, Any],
        engine: str = "MergeTree() ORDER BY tuple()",
        use_buffer: bool = False,
        buffer_size: int = 10000,
    ):
        """Initialize the repository.

        Args:
            model: Pydantic BaseModel class defining the schema.
            db_config: ClickHouse connection configuration.
            engine: ClickHouse table engine to use for creation.
            use_buffer: If True, inserts will be buffered until buffer_size is reached.
            buffer_size: Number of records to buffer before flushing.
        """
        self.model = model
        self.db_config = db_config
        self.table_name = getattr(model, "__tablename__", model.__name__.lower())
        self._sync = TableSync(model, db_config)

        self.use_buffer = use_buffer
        self.buffer_size = buffer_size
        self._buffer: List[BaseModel] = []

        # Automatic schema management
        self._sync.create_if_not_exists(engine=engine)
        self._sync.sync_with_model()

    def insert(self, data: BaseModel):
        """Insert a single record.

        If use_buffer is True, data is added to internal buffer.
        """
        if self.use_buffer:
            self._buffer.append(data)
            if len(self._buffer) >= self.buffer_size:
                self.flush()
        else:
            self.insert_many([data])

    def insert_many(self, data_list: List[BaseModel]):
        """Insert multiple records efficiently.

        If use_buffer is True, data is added to internal buffer.
        """
        if not data_list:
            return

        if self.use_buffer:
            self._buffer.extend(data_list)
            while len(self._buffer) >= self.buffer_size:
                chunk = self._buffer[: self.buffer_size]
                self._buffer = self._buffer[self.buffer_size :]
                self._real_insert_many(chunk)
        else:
            self._real_insert_many(data_list)

    def _real_insert_many(self, data_list: List[BaseModel]):
        """Internal method to perform actual database insertion."""
        client = get_client(self.db_config)
        data_to_insert = [list(item.model_dump().values()) for item in data_list]
        column_names = list(self.model.model_fields.keys())

        client.insert(self.table_name, data_to_insert, column_names=column_names)
        logger.debug("Inserted %d records into %s", len(data_list), self.table_name)

    def flush(self):
        """Force insertion of all records currently in the buffer."""
        if self._buffer:
            self._real_insert_many(self._buffer)
            self._buffer = []
            logger.info("Buffer flushed for %s", self.table_name)

    def insert_dataframe(self, df: Any):
        """Insert data from a Pandas DataFrame."""
        client = get_client(self.db_config)
        client.insert_df(self.table_name, df)
        logger.debug("Inserted DataFrame into %s", self.table_name)

    def insert_arrow(self, table: Any):
        """Insert data from an Apache Arrow Table.

        Args:
            table: pyarrow.Table instance.
        """
        if not HAS_ARROW:
            raise ImportError("pyarrow is required for insert_arrow")
        client = get_client(self.db_config)
        client.insert_arrow(self.table_name, table)
        logger.debug("Inserted Arrow Table into %s", self.table_name)

    def get_all(self) -> List[BaseModel]:
        """Retrieve all records."""
        client = get_client(self.db_config)
        query = f"SELECT * FROM {self.table_name}"
        result = client.query(query)

        return [
            self.model(**dict(zip(result.column_names, row)))
            for row in result.result_rows
        ]

    def get_first(self) -> Optional[BaseModel]:
        """Retrieve the first record."""
        client = get_client(self.db_config)
        query = f"SELECT * FROM {self.table_name} LIMIT 1"
        result = client.query(query)

        if not result.result_rows:
            return None

        return self.model(**dict(zip(result.column_names, result.result_rows[0])))

    def get_by_field(self, **filters) -> List[BaseModel]:
        """Get records filtered by specified fields."""
        if not filters:
            return self.get_all()

        conditions = " AND ".join(f"{key} = %({key})s" for key in filters)
        query = f"SELECT * FROM {self.table_name} WHERE {conditions}"
        return self.query(query, parameters=filters)

    def update(self, condition: str, **updates) -> None:
        """Update records matching a condition."""
        if not updates:
            return

        set_clause = ", ".join(f"{key} = %({key})s" for key in updates)
        query = f"ALTER TABLE {self.table_name} UPDATE {set_clause} WHERE {condition}"
        client = get_client(self.db_config)
        client.command(query, parameters=updates)
        logger.info("Update mutation started for %s", self.table_name)

    def delete(self, condition: str) -> None:
        """Delete records matching a condition."""
        query = f"ALTER TABLE {self.table_name} DELETE WHERE {condition}"
        client = get_client(self.db_config)
        client.command(query)
        logger.info("Delete mutation started for %s", self.table_name)

    def query(self, sql: str, parameters: Optional[Dict] = None) -> List[BaseModel]:
        """Execute a custom query and return model instances."""
        client = get_client(self.db_config)
        result = client.query(sql, parameters=parameters)

        return [
            self.model(**dict(zip(result.column_names, row)))
            for row in result.result_rows
        ]

    def query_arrow(self, sql: str, parameters: Optional[Dict] = None) -> Any:
        """Execute a custom query and return an Apache Arrow Table."""
        if not HAS_ARROW:
            raise ImportError("pyarrow is required for query_arrow")
        client = get_client(self.db_config)
        return client.query_arrow(sql, parameters=parameters)

    def query_stream(self, sql: str, parameters: Optional[Dict] = None):
        """Execute a custom query and yield model instances one by one.
        
        This is memory efficient for very large result sets.
        """
        client = get_client(self.db_config)
        # Use query_column_block_stream for maximum efficiency
        with client.query_row_block_stream(sql, parameters=parameters) as stream:
            for block in stream:
                for row in block:
                    yield self.model(**dict(zip(stream.source.column_names, row)))

    def count(self) -> int:
        """Get total record count."""
        client = get_client(self.db_config)
        result = client.command(f"SELECT count() FROM {self.table_name}")
        return int(result)

    def delete_all(self):
        """Truncate the table."""
        client = get_client(self.db_config)
        client.command(f"TRUNCATE TABLE {self.table_name}")

    def ping(self) -> bool:
        """Check if database is reachable."""
        try:
            client = get_client(self.db_config)
            return client.command("SELECT 1") == 1
        except Exception:
            return False

    # Async versions using asyncio.to_thread

    async def insert_async(self, data: BaseModel):
        """Asynchronously insert a single record."""
        await asyncio.to_thread(self.insert, data)

    async def insert_many_async(self, data_list: List[BaseModel]):
        """Asynchronously insert multiple records."""
        await asyncio.to_thread(self.insert_many, data_list)

    async def flush_async(self):
        """Asynchronously flush the buffer."""
        await asyncio.to_thread(self.flush)

    async def insert_dataframe_async(self, df: Any):
        """Asynchronously insert from DataFrame."""
        await asyncio.to_thread(self.insert_dataframe, df)

    async def insert_arrow_async(self, table: Any):
        """Asynchronously insert from Arrow Table."""
        await asyncio.to_thread(self.insert_arrow, table)

    async def get_all_async(self) -> List[BaseModel]:
        """Asynchronously retrieve all records."""
        return await asyncio.to_thread(self.get_all)

    async def get_first_async(self) -> Optional[BaseModel]:
        """Asynchronously retrieve the first record."""
        return await asyncio.to_thread(self.get_first)

    async def get_by_field_async(self, **filters) -> List[BaseModel]:
        """Asynchronously get records filtered by field."""
        return await asyncio.to_thread(self.get_by_field, **filters)

    async def update_async(self, condition: str, **updates):
        """Asynchronously update records."""
        await asyncio.to_thread(self.update, condition, **updates)

    async def delete_async(self, condition: str):
        """Asynchronously delete records."""
        await asyncio.to_thread(self.delete, condition)

    async def query_async(self, sql: str, parameters: Optional[Dict] = None) -> List[BaseModel]:
        """Asynchronously execute custom query."""
        return await asyncio.to_thread(self.query, sql, parameters)

    async def query_arrow_async(self, sql: str, parameters: Optional[Dict] = None) -> Any:
        """Asynchronously execute custom query returning Arrow Table."""
        return await asyncio.to_thread(self.query_arrow, sql, parameters)

    async def count_async(self) -> int:
        """Asynchronously count records."""
        return await asyncio.to_thread(self.count)

    async def ping_async(self) -> bool:
        """Asynchronously check database health."""
        return await asyncio.to_thread(self.ping)

    def __del__(self):
        """Ensure buffer is flushed when object is destroyed."""
        if hasattr(self, "_buffer") and self._buffer:
            try:
                self.flush()
            except Exception:
                pass
