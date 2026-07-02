from homelab_model import BaseModel


class Rule(BaseModel):
    api_groups: list[str]
    resources: list[str]
    verbs: list[str]


class Config(BaseModel):
    cluster: bool
    rules: list[Rule]
