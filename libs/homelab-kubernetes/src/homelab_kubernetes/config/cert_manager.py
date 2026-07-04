from homelab_model import BaseModel

from . import namespace


class Config(BaseModel):
    namespace: namespace.Config
    chart: str
    version: str
    issuer: str
    email: str
