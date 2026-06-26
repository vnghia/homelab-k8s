from homelab_types import BaseModel

from . import volume


class VolumesConfig(BaseModel):
    ephemeral: volume.ProvisioningVolume


class Config(BaseModel):
    disk: str
    image: str
    volumes: VolumesConfig
