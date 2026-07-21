from homelab_model import BaseModel

from . import certificate, cilium, gateway, policy


class Config(BaseModel):
    gateway: gateway.Config
    cilium: cilium.Config
    certificate: certificate.Config
    policy: policy.Config
