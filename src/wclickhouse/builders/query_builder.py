"""Advanced query builder for ClickHouse."""

from typing import Any, Optional


class QueryBuilder:
    """Builder for ClickHouse SQL queries."""

    def __init__(self, table_name: str):
        self._table_name = table_name
        self._select_fields: list[str] = ["*"]
        self._where_clauses: list[str] = []
        self._where_params: dict[str, Any] = {}
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._group_by: list[str] = []
        self._having: list[str] = []
        self._final: bool = False

    def select(self, *fields: str) -> "QueryBuilder":
        """Set fields to select."""
        self._select_fields = list(fields)
        return self

    def where(self, condition: str, **params) -> "QueryBuilder":
        """Add a WHERE clause."""
        self._where_clauses.append(condition)
        self._where_params.update(params)
        return self

    def order_by(self, field: str, desc: bool = False) -> "QueryBuilder":
        """Add ORDER BY clause."""
        self._order_by = f"{field} {'DESC' if desc else 'ASC'}"
        return self

    def limit(self, limit: int, offset: Optional[int] = None) -> "QueryBuilder":
        """Add LIMIT and optional OFFSET."""
        self._limit = limit
        self._offset = offset
        return self

    def group_by(self, *fields: str) -> "QueryBuilder":
        """Add GROUP BY."""
        self._group_by = list(fields)
        return self

    def having(self, condition: str) -> "QueryBuilder":
        """Add HAVING clause."""
        self._having.append(condition)
        return self

    def final(self) -> "QueryBuilder":
        """Add FINAL modifier (for CollapsingMergeTree, etc.)."""
        self._final = True
        return self

    def build(self) -> tuple[str, dict[str, Any]]:
        """Build the final SQL query and params."""
        query = f"SELECT {', '.join(self._select_fields)} FROM {self._table_name}"

        if self._final:
            query += " FINAL"

        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)

        if self._group_by:
            query += " GROUP BY " + ", ".join(self._group_by)

        if self._having:
            query += " HAVING " + " AND ".join(self._having)

        if self._order_by:
            query += f" ORDER BY {self._order_by}"

        if self._limit is not None:
            query += f" LIMIT {self._limit}"
            if self._offset is not None:
                query += f" OFFSET {self._offset}"

        return query, self._where_params
