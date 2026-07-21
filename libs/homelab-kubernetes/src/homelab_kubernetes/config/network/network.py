from homelab_model import BaseModel, JsonModel

from . import certificate, cilium, gateway


class Config(BaseModel):
    gateway: gateway.Config
    cilium: cilium.Config
    certificate: certificate.Config
    policies: dict[str, JsonModel]
