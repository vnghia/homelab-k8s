import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel
from pydantic import NonNegativeInt


class Config(BaseModel):
    container_port: NonNegativeInt

    def to_args(self, name: str) -> kubernetes.core.v1.ContainerPortArgs:
        return kubernetes.core.v1.ContainerPortArgs(
            name=name, container_port=self.container_port
        )
