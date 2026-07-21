from homelab_model import BaseModel

from . import features, install, network, stage


class Config(BaseModel):
    features: features.Config
    install: install.Config
    network: network.Config
    stage: stage.Config
