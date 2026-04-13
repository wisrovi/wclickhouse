"""Table synchronization with Pydantic models for ClickHouse."""

import asyncio
from typing import Dict, List

from wclickhouse.core.connection import get_client
from wclickhouse.utils.types import get_clickhouse_type


class TableSync:
    """Handles table synchronization between Pydantic models and ClickHouse (sync)."""

    def __init__(self, model, db_config: Dict):
        """Initialize table sync.

        Args:
            model: Pydantic BaseModel class.
            db_config: ClickHouse connection configuration.
        """
        self.model = model
        self.db_config = db_config
        self.table_name = getattr(model, "__tablename__", model.__name__.lower())

    def create_if_not_exists(self, engine: str = "MergeTree() ORDER BY tuple()"):
        """Create the table if it doesn't exist.

        Args:
            engine: ClickHouse engine to use. Default is MergeTree.
        """
        fields = ", ".join(
            f"{name} {get_clickhouse_type(info)}"
            for name, info in self.model.model_fields.items()
        )
        query = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields}) ENGINE = {engine}"
        )
        client = get_client(self.db_config)
        client.command(query)

    def sync_with_model(self):
        """Sync the table with the Pydantic model by adding new columns."""
        client = get_client(self.db_config)
        # Check existing columns using system.columns
        query = f"SELECT name FROM system.columns WHERE table = '{self.table_name}' AND database = '{client.database}'"
        result = client.query(query)
        existing_columns = {row[0] for row in result.result_rows}

        model_fields = set(self.model.model_fields.keys())
        new_fields = model_fields - existing_columns

        if new_fields:
            for field in new_fields:
                field_type = get_clickhouse_type(self.model.model_fields[field])
                alter_query = (
                    f"ALTER TABLE {self.table_name} ADD COLUMN {field} {field_type}"
                )
                client.command(alter_query)

    def table_exists(self) -> bool:
        """Check if the table exists."""
        client = get_client(self.db_config)
        query = f"EXISTS TABLE {self.table_name}"
        result = client.command(query)
        return bool(result)

    def drop_table(self):
        """Drop the table."""
        client = get_client(self.db_config)
        client.command(f"DROP TABLE IF EXISTS {self.table_name}")

    def get_columns(self) -> List[str]:
        """Get column names."""
        client = get_client(self.db_config)
        query = f"SELECT name FROM system.columns WHERE table = '{self.table_name}' AND database = '{client.database}'"
        result = client.query(query)
        return [row[0] for row in result.result_rows]

    # Async versions using asyncio.to_thread

    async def create_if_not_exists_async(
        self, engine: str = "MergeTree() ORDER BY tuple()"
    ):
        """Async version of create_if_not_exists."""
        await asyncio.to_thread(self.create_if_not_exists, engine)

    async def sync_with_model_async(self):
        """Async version of sync_with_model."""
        await asyncio.to_thread(self.sync_with_model)

    async def table_exists_async(self) -> bool:
        """Async version of table_exists."""
        return await asyncio.to_thread(self.table_exists)

    async def drop_table_async(self):
        """Async version of drop_table."""
        await asyncio.to_thread(self.drop_table)

    async def get_columns_async(self) -> List[str]:
        """Async version of get_columns."""
        return await asyncio.to_thread(self.get_columns)
