from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    spec: JsonModel
