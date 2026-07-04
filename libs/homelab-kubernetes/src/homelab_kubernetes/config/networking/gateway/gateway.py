from homelab_model import BaseModel

from . import crd


class Config(BaseModel):
    crd: crd.Config
