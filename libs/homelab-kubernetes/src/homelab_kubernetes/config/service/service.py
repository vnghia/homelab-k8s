from homelab_model import BaseModel

from . import account


class Config(BaseModel):
    accounts: dict[str, account.Config]
