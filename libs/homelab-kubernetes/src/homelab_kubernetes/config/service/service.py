from homelab_model import BaseModel

from . import account, deployment


class Config(BaseModel):
    accounts: dict[str, account.Config]
    deployments: dict[str, deployment.Config]
