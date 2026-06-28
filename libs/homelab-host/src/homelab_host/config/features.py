from homelab_model import BaseModel


class Config(BaseModel):
    controlplane: bool
    worker: bool
    loadbalancer: bool
