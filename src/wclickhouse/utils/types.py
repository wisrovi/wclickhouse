"""ClickHouse type mapping from Pydantic fields."""

import datetime
from typing import Any, Union, get_args, get_origin

from pydantic.fields import FieldInfo


def get_clickhouse_type(field: FieldInfo) -> str:
    """Convert Pydantic field type to ClickHouse type.

    Args:
        field: Pydantic field info object.

    Returns:
        str: ClickHouse type string.
    """
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
    }

    # Handle Optional (Union[T, None])
    if origin is Union:
        # Check if it's Optional[T]
        if type(None) in args:
            actual_type = args[0] if args[1] is type(None) else args[1]
            # Recursive call with modified annotation to handle nested types in Optional
            # But for simplicity, we map it to Nullable
            inner_type = _map_primitive(actual_type, type_mapping)
            return f"Nullable({inner_type})"

    # Handle List[T] -> Array(T)
    if origin is list or origin is list:
        inner_type = _map_primitive(args[0], type_mapping)
        return f"Array({inner_type})"

    return _map_primitive(annotation, type_mapping)


def _map_primitive(typ: Any, mapping: dict) -> str:
    """Helper to map primitive types."""
    if typ in mapping:
        return mapping[typ]
    return "String"  # Default to String for unknown types
