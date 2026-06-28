from homelab_types import BaseModel

from . import gateway


class Config(BaseModel):
    gateway: gateway.Config
