from enum import StrEnum, auto
from ipaddress import IPv4Address

from homelab_types import BaseModel


class IpsConfig(BaseModel):
    tailscale: IPv4Address


class VolumeConfig(BaseModel):
    selector: str
    max_size: str | None


class InstallVolumesConfig(BaseModel):
    ephemeral: VolumeConfig


class InstallConfig(BaseModel):
    disk: str
    image: str
    volumes: InstallVolumesConfig


class FeaturesConfig(BaseModel):
    controlplane: bool
    worker: bool
    loadbalancer: bool


class StageConfig(StrEnum):
    INITIAL = auto()
    READY = auto()


class Config(BaseModel):
    ips: IpsConfig
    features: FeaturesConfig
    install: InstallConfig
    stage: StageConfig
