from homelab_model import BaseModel


class Config(BaseModel):
    extensions: list[str]
