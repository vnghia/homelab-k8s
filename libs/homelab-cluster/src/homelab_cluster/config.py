from enum import StrEnum, auto

from homelab_types import BaseModel


class VersionConfig(BaseModel):
    talos: str
    k8s: str


class ImageConfig(BaseModel):
    extensions: list[str]


class HostInstallConfig(BaseModel):
    disk: str
    image: str


class HostFeaturesConfig(BaseModel):
    controlplane: bool
    worker: bool
    loadbalancer: bool


class HostStageConfig(StrEnum):
    INITIAL = auto()
    READY = auto()


class HostConfig(BaseModel):
    endpoint: str
    features: HostFeaturesConfig
    install: HostInstallConfig
    stage: HostStageConfig


class ClusterConfig(BaseModel):
    name: str
    endpoint: str
    version: VersionConfig
    images: dict[str, ImageConfig]
    hosts: dict[str, HostConfig]
