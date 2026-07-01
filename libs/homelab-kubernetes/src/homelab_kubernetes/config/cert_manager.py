from homelab_model import BaseModel


class Config(BaseModel):
    namespace: str
    chart: str
    version: str
