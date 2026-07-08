from homelab_model import BaseModel

from .. import namespace
from . import account, custom_resource, deployment, secret, service


class Config(BaseModel):
    namespace: namespace.Config
    accounts: dict[str, account.Config]
    secrets: dict[str, secret.Config]
    custom_resources: dict[str, custom_resource.Config]
    deployments: dict[str, deployment.Config]
    services: dict[str, service.Config]
