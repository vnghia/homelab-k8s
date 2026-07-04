from homelab_model import BaseModel

from ... import namespace
from . import cilium, crd, listener


class Gateway(BaseModel):
    class_: str
    listeners: dict[str, listener.Config]


class Config(BaseModel):
    crd: crd.Config
    namespace: namespace.Config
    cilium: cilium.Config
    gateways: dict[str, Gateway]
