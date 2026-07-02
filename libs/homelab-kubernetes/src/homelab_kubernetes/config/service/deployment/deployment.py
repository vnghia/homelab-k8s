from homelab_model import BaseModel

from . import container


class Config(BaseModel):
    account: str | None
    containers: dict[str, container.Config]
