from typing import Any


def resolve[T](data: Any, resolve_key: str, resolve_type: type[T]) -> T:
    result = data
    for key in resolve_key.split("."):
        result = result[key]
    if type(result) != resolve_type:
        raise TypeError(f"Expecting an instance of type {resolve_type}, got {result}")
    return result
