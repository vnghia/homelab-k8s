from homelab_types import BaseModel

from . import domain, networking


class Config(BaseModel):
    version: str
    domain: domain.Config
    networking: networking.Config
