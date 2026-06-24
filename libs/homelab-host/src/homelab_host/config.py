from homelab_types import BaseModel, RootModel


class ImageConfig(BaseModel):
    version: str
    extensions: list[str]


class HostConfig(BaseModel):
    address: str
    image: ImageConfig


class HostsConfig(RootModel[dict[str, HostConfig]]):
    pass
