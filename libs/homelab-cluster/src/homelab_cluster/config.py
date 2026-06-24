from homelab_types import BaseModel


class ImageConfig(BaseModel):
    extensions: list[str]


class HostConfig(BaseModel):
    address: str
    image: ImageConfig


class ClusterConfig(BaseModel):
    name: str
    version: str
    endpoint: str
    hosts: dict[str, HostConfig]
