from homelab_model import BaseModel

from . import features, install, ips, stage


class Config(BaseModel):
    ips: ips.Config
    features: features.Config
    install: install.Config
    stage: stage.Config
