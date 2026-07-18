from homelab_model import BaseModel

from .. import custom_resource, namespace
from . import account, chart, deployment, secret, service


class Config(BaseModel):
    namespace: namespace.Config
    accounts: dict[str, account.Config]
    secrets: dict[str, secret.Config]
    charts: dict[str, chart.Config]
    custom_resources: dict[str, custom_resource.Config]
    deployments: dict[str, deployment.Config]
    services: dict[str, service.Config]
