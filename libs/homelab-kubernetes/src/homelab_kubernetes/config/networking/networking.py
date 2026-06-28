from homelab_model import BaseModel

from . import gateway


class Config(BaseModel):
    gateway: gateway.Config
