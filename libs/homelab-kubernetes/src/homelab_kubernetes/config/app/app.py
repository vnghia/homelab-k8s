from homelab_model import BaseModel

from .. import namespace
from . import account, deployment, secret, service


class Config(BaseModel):
    namespace: namespace.Config
    accounts: dict[str, account.Config]
    secrets: dict[str, secret.Config]
    deployments: dict[str, deployment.Config]
    services: dict[str, service.Config]
