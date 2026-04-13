"""Main repository class for ClickHouse operations."""

import asyncio
import logging
from typing import Any, Optional

from pydantic import BaseModel

from wclickhouse.core.connection import get_client
from wclickhouse.core.sync import TableSync

logger = logging.getLogger(__name__)


class WClickHouse:
    """ClickHouse repository using Pydantic models.

    Provides a simple interface for CRUD and analytical operations on ClickHouse,
    optimized for bulk inserts and Pydantic validation.
    """

    def __init__(
        self,
        model: type[BaseModel],
        db_config: dict[str, Any],
        engine: str = "MergeTree() ORDER BY tuple()",
    ):
        """Initialize the repository.

        Args:
            model: Pydantic BaseModel class defining the schema.
            db_config: ClickHouse connection configuration.
            engine: ClickHouse table engine to use for creation.
        """
        self.model = model
        self.db_config = db_config
        self.table_name = getattr(model, "__tablename__", model.__name__.lower())
        self._sync = TableSync(model, db_config)

        # Automatic schema management
        self._sync.create_if_not_exists(engine=engine)
        self._sync.sync_with_model()

    def insert(self, data: BaseModel):
        """Insert a single record.

        Note: ClickHouse performs better with bulk inserts. Use insert_many for high volume.
        """
        self.insert_many([data])

    def insert_many(self, data_list: list[BaseModel]):
        """Insert multiple records efficiently.

        Args:
            data_list: List of Pydantic model instances.
        """
        if not data_list:
            return

        client = get_client(self.db_config)
        data_to_insert = [list(item.model_dump().values()) for item in data_list]
        column_names = list(self.model.model_fields.keys())

        client.insert(self.table_name, data_to_insert, column_names=column_names)
        logger.debug("Inserted %d records into %s", len(data_list), self.table_name)

    def insert_dataframe(self, df: Any):
        """Insert data from a Pandas DataFrame.

        Args:
            df: Pandas DataFrame instance.
        """
        client = get_client(self.db_config)
        client.insert_df(self.table_name, df)
        logger.debug("Inserted DataFrame into %s", self.table_name)

    def get_all(self) -> list[BaseModel]:
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

    def get_by_field(self, **filters) -> list[BaseModel]:
        """Get records filtered by specified fields.

        Note: This uses standard WHERE clause.
        """
        if not filters:
            return self.get_all()

        conditions = " AND ".join(f"{key} = %({key})s" for key in filters)
        query = f"SELECT * FROM {self.table_name} WHERE {conditions}"
        return self.query(query, parameters=filters)

    def update(self, condition: str, **updates) -> None:
        """Update records matching a condition.

        Note: ClickHouse updates are asynchronous mutations.
        Example: db.update("id = 1", name="new_name")
        """
        if not updates:
            return

        set_clause = ", ".join(f"{key} = %({key})s" for key in updates)
        query = f"ALTER TABLE {self.table_name} UPDATE {set_clause} WHERE {condition}"
        client = get_client(self.db_config)
        client.command(query, parameters=updates)
        logger.info("Update mutation started for %s", self.table_name)

    def delete(self, condition: str) -> None:
        """Delete records matching a condition.

        Note: ClickHouse deletes are asynchronous mutations.
        Example: db.delete("id = 1")
        """
        query = f"ALTER TABLE {self.table_name} DELETE WHERE {condition}"
        client = get_client(self.db_config)
        client.command(query)
        logger.info("Delete mutation started for %s", self.table_name)

    def query(self, sql: str, parameters: Optional[dict] = None) -> list[BaseModel]:
        """Execute a custom query and return model instances.

        Args:
            sql: SQL query string.
            parameters: Optional parameters for the query.
        """
        client = get_client(self.db_config)
        result = client.query(sql, parameters=parameters)

        return [
            self.model(**dict(zip(result.column_names, row)))
            for row in result.result_rows
        ]

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

    async def insert_many_async(self, data_list: list[BaseModel]):
        """Asynchronously insert multiple records."""
        await asyncio.to_thread(self.insert_many, data_list)

    async def insert_dataframe_async(self, df: Any):
        """Asynchronously insert from DataFrame."""
        await asyncio.to_thread(self.insert_dataframe, df)

    async def get_all_async(self) -> list[BaseModel]:
        """Asynchronously retrieve all records."""
        return await asyncio.to_thread(self.get_all)

    async def query_async(
        self, sql: str, parameters: Optional[dict] = None
    ) -> list[BaseModel]:
        """Asynchronously execute custom query."""
        return await asyncio.to_thread(self.query, sql, parameters)

    async def count_async(self) -> int:
        """Asynchronously count records."""
        return await asyncio.to_thread(self.count)

    async def get_first_async(self) -> Optional[BaseModel]:
        """Asynchronously retrieve the first record."""
        return await asyncio.to_thread(self.get_first)

    async def get_by_field_async(self, **filters) -> list[BaseModel]:
        """Asynchronously get records filtered by field."""
        return await asyncio.to_thread(self.get_by_field, **filters)

    async def update_async(self, condition: str, **updates):
        """Asynchronously update records."""
        await asyncio.to_thread(self.update, condition, **updates)

    async def delete_async(self, condition: str):
        """Asynchronously delete records."""
        await asyncio.to_thread(self.delete, condition)

    async def ping_async(self) -> bool:
        """Asynchronously check database health."""
        return await asyncio.to_thread(self.ping)
