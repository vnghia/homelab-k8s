from homelab_types import BaseModel

from . import domain


class Config(BaseModel):
    version: str
    domain: domain.Config
