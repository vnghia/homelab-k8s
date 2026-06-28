from homelab_types import BaseModel

from . import image, machine


class Config(BaseModel):
    version: str
    bootstrap: str
    images: dict[str, image.Config]
    machines: dict[str, machine.Config]
