from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    namespace: str
    kustomization: JsonModel
