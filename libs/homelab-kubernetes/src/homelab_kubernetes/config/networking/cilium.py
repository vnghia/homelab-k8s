from homelab_model import BaseModel, JsonModel

from .. import namespace


class Config(BaseModel):
    namespace: namespace.Config
    kustomization: JsonModel
