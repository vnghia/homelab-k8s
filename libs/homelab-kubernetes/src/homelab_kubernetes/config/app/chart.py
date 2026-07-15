from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    chart: str
    version: str
    skip_crds: bool
    values: JsonModel
