from homelab_model import BaseModel

from . import cluster, interface


class Config(BaseModel):
    interfaces: dict[str, interface.Config]
    cluster: cluster.Config
