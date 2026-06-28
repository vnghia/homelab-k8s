from homelab_model import BaseModel

from . import domain, networking


class Config(BaseModel):
    version: str
    domain: domain.Config
    networking: networking.Config
