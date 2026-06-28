from typing import Any

from homelab_model import BaseModel


class Config(BaseModel):
    namespace: str
    manifests: list[Any]
