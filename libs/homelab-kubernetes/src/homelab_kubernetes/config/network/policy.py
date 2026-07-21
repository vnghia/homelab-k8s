from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    cluster: dict[str, JsonModel]
