from homelab_types import BaseModel


class ImageConfig(BaseModel):
    extensions: list[str]


class HostConfig(BaseModel):
    address: str
    image: ImageConfig


class ClusterConfig(BaseModel):
    version: str
    hosts: dict[str, HostConfig]
