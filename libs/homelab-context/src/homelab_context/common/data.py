from typing import Any

import homelab_common as common
from pulumi import Output


def resolve[T](data: Any, resolve_type: type[T], resolve_path: str) -> T | Output[T]:
    data = common.data.traverse_resolve_path(data, resolve_path)
    if checked_data := common.data.check_resolve_type(data, resolve_type, False):
        return checked_data
    return Output.from_input(data).apply(
        lambda data: common.data.check_resolve_type(data, resolve_type, True),
    )
