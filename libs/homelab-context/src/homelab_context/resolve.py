import typing
from enum import StrEnum, auto
from typing import Any, Literal

import homelab_common as common


class ResolveSource(StrEnum):
    PULUMI_SECRETS = "pulumi/secrets"


class ResolveType(StrEnum):
    STR = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()

    def pytype(self) -> type:
        match self:
            case self.STR:
                return str
            case self.BOOL:
                return bool
            case self.INT:
                return int
            case self.FLOAT:
                return float


@typing.overload
def resolve(
    data: Any, resolve_key: str, resolve_type: Literal[ResolveType.STR]
) -> str: ...


@typing.overload
def resolve(
    data: Any, resolve_key: str, resolve_type: Literal[ResolveType.BOOL]
) -> bool: ...


@typing.overload
def resolve(
    data: Any, resolve_key: str, resolve_type: Literal[ResolveType.INT]
) -> int: ...


@typing.overload
def resolve(
    data: Any, resolve_key: str, resolve_type: Literal[ResolveType.FLOAT]
) -> float: ...


@typing.overload
def resolve(
    data: Any, resolve_key: str, resolve_type: ResolveType
) -> str | bool | int | float: ...


def resolve(
    data: Any, resolve_key: str, resolve_type: ResolveType
) -> str | bool | int | float:
    match resolve_type:
        case ResolveType.STR:
            return common.data.resolve(data, resolve_key, str)
        case ResolveType.BOOL:
            return common.data.resolve(data, resolve_key, bool)
        case ResolveType.INT:
            return common.data.resolve(data, resolve_key, int)
        case ResolveType.FLOAT:
            return common.data.resolve(data, resolve_key, float)
