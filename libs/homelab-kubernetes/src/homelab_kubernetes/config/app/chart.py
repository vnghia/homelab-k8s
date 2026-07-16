from homelab_model import BaseModel, JsonModel


class Repository(BaseModel):
    repo: str


class Config(BaseModel):
    chart: str
    version: str
    skip_crds: bool
    repository: Repository | None
    values: JsonModel
