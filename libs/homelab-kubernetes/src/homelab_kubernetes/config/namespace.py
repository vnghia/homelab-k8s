from homelab_model import BaseModel

from . import security


class Config(BaseModel):
    securities: dict[security.Mode, security.Level] = {}
