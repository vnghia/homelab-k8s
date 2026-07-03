from homelab_model import BaseModel


class Config(BaseModel):
    repo: str
    tag: str

    @property
    def image(self) -> str:
        return f"{self.repo}:{self.tag}"
