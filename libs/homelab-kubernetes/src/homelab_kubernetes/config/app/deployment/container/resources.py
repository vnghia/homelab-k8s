import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel


class Config(BaseModel):
    requests: dict[str, str]
    limits: dict[str, str]

    def to_args(self) -> kubernetes.core.v1.ResourceRequirementsArgs:
        return kubernetes.core.v1.ResourceRequirementsArgs(requests=self.requests, limits=self.limits)
