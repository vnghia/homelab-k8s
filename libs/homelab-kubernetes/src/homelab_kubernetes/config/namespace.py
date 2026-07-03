from homelab_model import BaseModel

from . import security


class Config(BaseModel):
    securities: dict[security.Mode, security.Level]

    def to_labels(self) -> dict[str, str]:
        return {mode.label: level for mode, level in self.securities.items()}
