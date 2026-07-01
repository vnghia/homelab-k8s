from homelab_model import BaseModel

from . import zone


class Config(BaseModel):
    zones: dict[str, zone.Config]
