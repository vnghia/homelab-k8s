from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    cluster: bool
    api_version: str
    kind: str
    spec: JsonModel
