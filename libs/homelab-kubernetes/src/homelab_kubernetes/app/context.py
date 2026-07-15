import homelab_context as context
from pydantic import dataclasses


@dataclasses.dataclass
class Context(context.Context):
    name: str
