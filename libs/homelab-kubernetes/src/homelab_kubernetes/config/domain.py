from homelab_model import BaseModel


class Config(BaseModel):
    cluster: str
    name: str
