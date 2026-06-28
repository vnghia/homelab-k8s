from homelab_model import BaseModel


class Config(BaseModel):
    version: str
    type: str
