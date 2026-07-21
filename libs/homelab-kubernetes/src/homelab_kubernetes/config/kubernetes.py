from homelab_model import BaseModel

from . import app, domain, network


class Config(BaseModel):
    version: str
    domain: domain.Config
    network: network.Config
    apps: dict[str, app.Config]
