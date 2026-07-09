import typing
from typing import Any, Literal

from pulumi import Output

from .. import common
from . import type


@typing.overload
def resolve(
    data: Any, resolve_type: Literal[type.Type.STR], resolve_path: str,
) -> str | Output[str]: ...


@typing.overload
def resolve(
    data: Any, resolve_type: Literal[type.Type.BOOL], resolve_path: str,
) -> bool | Output[bool]: ...


@typing.overload
def resolve(
    data: Any, resolve_type: Literal[type.Type.INT], resolve_path: str,
) -> int | Output[int]: ...


@typing.overload
def resolve(
    data: Any, resolve_type: Literal[type.Type.FLOAT], resolve_path: str,
) -> float | Output[float]: ...


@typing.overload
def resolve(
    data: Any, resolve_type: type.Type, resolve_path: str,
) -> type.PythonType | Output[type.PythonType]: ...


def resolve(
    data: Any, resolve_type: type.Type, resolve_path: str,
) -> type.PythonType | Output[type.PythonType]:
    match resolve_type:
        case type.Type.STR:
            return common.data.resolve(data, str, resolve_path)
        case type.Type.BOOL:
            return common.data.resolve(data, bool, resolve_path)
        case type.Type.INT:
            return common.data.resolve(data, int, resolve_path)
        case type.Type.FLOAT:
            return common.data.resolve(data, float, resolve_path)
