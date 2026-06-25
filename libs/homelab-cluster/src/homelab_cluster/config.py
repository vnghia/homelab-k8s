from homelab_types import BaseModel


class VersionConfig(BaseModel):
    talos: str
    k8s: str


class ImageConfig(BaseModel):
    extensions: list[str]


class HostInstallConfig(BaseModel):
    disk: str
    image: str


class HostConfig(BaseModel):
    endpoint: str
    controlplane: bool
    worker: bool
    install: HostInstallConfig


class ClusterConfig(BaseModel):
    name: str
    endpoint: str
    version: VersionConfig
    images: dict[str, ImageConfig]
    hosts: dict[str, HostConfig]
