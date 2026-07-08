from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    api_version: str
    kind: str
    spec: JsonModel
