from homelab_model import BaseModel
from pydantic import NonNegativeInt


class ContainerPort(BaseModel):
    container: str
    port: str


class Port(BaseModel):
    port: NonNegativeInt | None
    container: ContainerPort


class Config(BaseModel):
    deployment: str
    ports: dict[str, Port]
