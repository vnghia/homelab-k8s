from homelab_model import BaseModel

from .. import namespace
from . import account, deployment, service


class Namespace(BaseModel):
    name: str | None
    config: namespace.Config


class Config(BaseModel):
    namespace: Namespace
    accounts: dict[str, account.Config]
    deployments: dict[str, deployment.Config]
    services: dict[str, service.Config]
