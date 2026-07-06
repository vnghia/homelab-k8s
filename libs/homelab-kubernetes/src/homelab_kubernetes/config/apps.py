from homelab_model import BaseModel

from . import app, cert_manager


class Config(BaseModel):
    cert_manager: cert_manager.Config
    apps: dict[str, app.Config]
