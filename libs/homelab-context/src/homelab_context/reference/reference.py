from typing import Any

from pydantic import TypeAdapter, ValidationError

from . import pulumi

Reference = pulumi.Pulumi


Adapter = TypeAdapter(Reference)


def recursive_validate(data: Any) -> Any:
    if isinstance(data, list):
        return [recursive_validate(item) for item in data]
    if isinstance(data, dict):
        try:
            return Adapter.validate_python(data, extra="forbid")
        except ValidationError:
            return {key: recursive_validate(value) for key, value in data.items()}
    return data
