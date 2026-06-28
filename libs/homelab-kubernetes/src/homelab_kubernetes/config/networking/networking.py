from homelab_model import BaseModel

from . import cilium, gateway


class Config(BaseModel):
    gateway: gateway.Config
    cilium: cilium.Config
