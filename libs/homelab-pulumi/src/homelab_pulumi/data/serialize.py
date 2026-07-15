from collections.abc import Callable
from typing import Any

import orjson
import yaml_rs
from homelab_context import Context
from pulumi import Output


def default_dumper(data: Any) -> str:
    return orjson.dumps(data).decode()


def serialize(
    context: Context, data: Any, *, direct: bool, dumper: Callable[[Any], str] | None = None
) -> str | Output[str]:
    dumper_ = dumper or default_dumper
    if direct:
        return dumper_(data)
    return Output.from_input(data).apply(dumper_)


def yaml(context: Context, data: Any, *, direct: bool) -> str | Output[str]:
    return serialize(
        context,
        data,
        direct=direct,
        dumper=lambda data: (
            "\n".join([yaml_rs.dumps(item) for item in data]) if isinstance(data, list) else yaml_rs.dumps(data)
        ),
    )
