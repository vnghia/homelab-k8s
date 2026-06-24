from homelab_types import BaseModel


class ImageConfig(BaseModel):
    version: str
    extensions: list[str]


class HostConfig(BaseModel):
    address: str
    image: ImageConfig


class ClusterConfig(BaseModel):
    hosts: dict[str, HostConfig]
