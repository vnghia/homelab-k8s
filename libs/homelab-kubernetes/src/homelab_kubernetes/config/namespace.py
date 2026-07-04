from homelab_model import BaseModel
from pulumi import Output

from . import security


class Spec(BaseModel):
    securities: dict[security.Mode, security.Level]

    def to_labels(self) -> dict[str, str | Output[str]]:
        return {mode.label: level for mode, level in self.securities.items()}


class Config(BaseModel):
    name: str
    spec: Spec
