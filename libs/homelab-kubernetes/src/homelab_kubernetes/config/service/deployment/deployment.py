from homelab_model import BaseModel

from . import container, security_context


class Config(BaseModel):
    account: str | None
    security_context: security_context.Config
    containers: dict[str, container.Config]
