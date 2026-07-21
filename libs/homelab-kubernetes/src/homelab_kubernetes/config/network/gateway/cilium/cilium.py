from homelab_model import BaseModel

from . import class_


class Config(BaseModel):
    classes: dict[str, class_.Config]
