from homelab_types import BaseModel


class ImageConfig(BaseModel):
    extensions: list[str]


class HostConfig(BaseModel):
    address: str
    image: str


class ClusterConfig(BaseModel):
    name: str
    version: str
    endpoint: str
    images: dict[str, ImageConfig]
    hosts: dict[str, HostConfig]
