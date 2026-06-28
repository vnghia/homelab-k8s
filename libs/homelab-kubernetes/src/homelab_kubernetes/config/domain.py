from homelab_model import BaseModel


class Config(BaseModel):
    prefix: str | None
    name: str
