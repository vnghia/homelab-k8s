from homelab_model import BaseModel


class Image(BaseModel):
    repo: str
    tag: str

    @property
    def image(self) -> str:
        return f"{self.repo}:{self.tag}"


class Config(BaseModel):
    image: Image
    env: dict[str, str]
