from homelab_types import BaseModel


class Config(BaseModel):
    version: str
    type: str
