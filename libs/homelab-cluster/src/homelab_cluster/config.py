import functools
from enum import StrEnum, auto

from homelab_common import string
from homelab_pulumi.constant import STACK
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
    features: HostFeaturesConfig
    install: HostInstallConfig
    stage: HostStageConfig


class ClusterDomainConfig(BaseModel):
    prefix: str | None
    name: str


class ClusterConfig(BaseModel):
    name: str
    bootstrap: str
    domain: ClusterDomainConfig
    version: VersionConfig
    images: dict[str, ImageConfig]
    hosts: dict[str, HostConfig]

    @functools.cached_property
    def endpoint(self) -> str:
        return f"https://{
            string.add_prefix(
                STACK,
                string.add_prefix(self.domain.prefix, self.domain.name, separator='.'),
                separator='.',
            )
        }:6443"
