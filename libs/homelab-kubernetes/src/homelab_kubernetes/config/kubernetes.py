from homelab_model import BaseModel

from . import app, domain, label, network


class Config(BaseModel):
    version: str
    domain: domain.Config
    label: label.Config
    network: network.Config
    apps: dict[str, app.Config]
