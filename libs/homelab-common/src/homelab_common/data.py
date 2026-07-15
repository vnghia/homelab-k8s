import typing
from typing import Any, Literal


@typing.overload
def check_resolve_type[T](
    data: Any,
    resolve_type: type[T],
    raise_error: Literal[True],
) -> T: ...


@typing.overload
def check_resolve_type[T](
    data: Any,
    resolve_type: type[T],
    raise_error: Literal[False],
) -> T | None: ...


def check_resolve_type[T](
    data: Any,
    resolve_type: type[T],
    raise_error: bool,
) -> T | None:
    if not isinstance(data, resolve_type):
        if raise_error:
            raise TypeError(f"Expecting an instance of type {resolve_type}, got {data}")
        return None
    return data


def traverse_resolve_path(data: Any, resolve_path: str) -> Any:
    for key in resolve_path.split("."):
        data = data[key] if isinstance(data, dict) else getattr(data, key)
    return data


def resolve[T](data: dict[str, Any], resolve_type: type[T], resolve_path: str) -> T:
    return check_resolve_type(
        traverse_resolve_path(data, resolve_path),
        resolve_type,
        True,
    )
