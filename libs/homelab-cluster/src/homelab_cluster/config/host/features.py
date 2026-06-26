from homelab_types import BaseModel


class Config(BaseModel):
    controlplane: bool
    worker: bool
    loadbalancer: bool
