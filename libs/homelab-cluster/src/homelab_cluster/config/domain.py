from homelab_types import BaseModel


class Config(BaseModel):
    prefix: str | None
    name: str
