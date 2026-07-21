from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    policies: dict[str, JsonModel]
