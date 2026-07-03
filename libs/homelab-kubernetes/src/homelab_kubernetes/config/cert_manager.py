from homelab_model import BaseModel

from . import namespace


class Namespace(BaseModel):
    name: str
    config: namespace.Config


class Config(BaseModel):
    namespace: Namespace
    chart: str
    version: str
    issuer: str
    email: str
