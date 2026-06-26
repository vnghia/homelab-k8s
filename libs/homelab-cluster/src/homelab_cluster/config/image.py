from homelab_types import BaseModel


class Config(BaseModel):
    extensions: list[str]
