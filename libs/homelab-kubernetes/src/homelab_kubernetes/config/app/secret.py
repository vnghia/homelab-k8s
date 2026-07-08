from homelab_model import BaseModel, JsonModel


class Config(BaseModel):
    type: str
    string_data: JsonModel
