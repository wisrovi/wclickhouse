"""ClickHouse type mapping from Pydantic fields."""

import datetime
import decimal
from enum import Enum
from typing import Any, Union, get_args, get_origin

from pydantic.fields import FieldInfo


def get_clickhouse_type(field: FieldInfo) -> str:
    """Convert Pydantic field type to ClickHouse type.

    Args:
        field: Pydantic field info object.

    Returns:
        str: ClickHouse type string.
    """
    # 1. Manual override check
    if field.json_schema_extra and "clickhouse_type" in field.json_schema_extra:
        return field.json_schema_extra["clickhouse_type"]

    annotation = field.annotation
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Basic types mapping
    type_mapping = {
        int: "Int64",
        str: "String",
        float: "Float64",
        bool: "Bool",
        datetime.datetime: "DateTime64(3)",
        datetime.date: "Date",
        decimal.Decimal: "Decimal(18, 4)",
    }

    # Handle Optional (Union[T, None])
    if origin is Union:
        if type(None) in args:
            actual_type = args[0] if args[1] is type(None) else args[1]
            inner_type = _map_primitive(actual_type, type_mapping)
            return f"Nullable({inner_type})"

    # Handle List[T] -> Array(T)
    if origin is list:
        inner_type = _map_primitive(args[0], type_mapping)
        return f"Array({inner_type})"

    # Handle Dict[K, V] -> Map(K, V)
    if origin is dict:
        key_type = _map_primitive(args[0], type_mapping)
        val_type = _map_primitive(args[1], type_mapping)
        return f"Map({key_type}, {val_type})"

    return _map_primitive(annotation, type_mapping)


def _map_primitive(typ: Any, mapping: dict) -> str:
    """Helper to map primitive types."""
    if typ in mapping:
        return mapping[typ]

    # Handle Enums
    if isinstance(typ, type) and issubclass(typ, Enum):
        return "String"

    return "String"  # Default to String for unknown types
