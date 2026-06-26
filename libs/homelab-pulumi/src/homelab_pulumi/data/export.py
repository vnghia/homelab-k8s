from typing import Any

import pulumi


def export(name: str, value: Any) -> None:
    pulumi.export(name, value)
