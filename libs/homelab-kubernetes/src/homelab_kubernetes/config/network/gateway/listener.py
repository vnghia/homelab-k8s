from homelab_model import BaseModel
from pydantic import NonNegativeInt


class Config(BaseModel):
    protocol: str
    port: NonNegativeInt
