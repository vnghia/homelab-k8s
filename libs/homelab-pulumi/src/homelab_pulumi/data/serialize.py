from collections.abc import Callable
from typing import Any

import orjson
import yaml_rs
from pulumi import Output

DEFAULT_LOADER: Callable[[str], Any] = orjson.loads
DEFAULT_DUMPER: Callable[[Any], str] = lambda data: orjson.dumps(data).decode()


def serialize(
    data: Any,
    direct: bool,
    *,
    loader: Callable[[str], Any] | None = None,
    dumper: Callable[[Any], str] | None = None,
) -> str | Output[str]:

    loader_ = loader or DEFAULT_LOADER
    dumper_ = dumper or DEFAULT_DUMPER
    if direct:
        return dumper_(data)
    return Output.json_dumps(data).apply(lambda data: dumper_(loader_(data)))


def yaml(data: Any, direct: bool) -> str | Output[str]:
    return serialize(data, direct, dumper=yaml_rs.dumps)
