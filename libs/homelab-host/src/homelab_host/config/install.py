from homelab_model import BaseModel

from . import volume


class VolumesConfig(BaseModel):
    ephemeral: volume.ProvisioningVolume


class Config(BaseModel):
    disk: str
    image: str
    volumes: VolumesConfig
