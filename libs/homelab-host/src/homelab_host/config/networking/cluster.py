from homelab_model import BaseModel


class Config(BaseModel):
    pod_subnets: list[str]
