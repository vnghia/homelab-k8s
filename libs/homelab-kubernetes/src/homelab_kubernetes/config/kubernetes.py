from homelab_model import BaseModel

from . import app, domain, networking


class Config(BaseModel):
    version: str
    domain: domain.Config
    networking: networking.Config
    apps: dict[str, app.Config]
