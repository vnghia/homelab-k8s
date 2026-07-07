from typing import Any


def resolve[T](data: Any, resolve_type: type[T], resolve_path: str) -> T:
    result = data
    for key in resolve_path.split("."):
        result = result[key]
    if type(result) != resolve_type:
        raise TypeError(f"Expecting an instance of type {resolve_type}, got {result}")
    return result
