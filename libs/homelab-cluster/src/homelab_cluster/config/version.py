from homelab_types import BaseModel


class Config(BaseModel):
    talos: str
    k8s: str
