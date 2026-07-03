from homelab_model import BaseModel

from . import app, cert_manager, domain, networking


class Config(BaseModel):
    version: str
    domain: domain.Config
    networking: networking.Config
    cert_manager: cert_manager.Config
    apps: dict[str, app.Config]
