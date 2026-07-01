from homelab_model import BaseModel

from . import features, install, networking, stage


class Config(BaseModel):
    features: features.Config
    install: install.Config
    networking: networking.Config
    stage: stage.Config
