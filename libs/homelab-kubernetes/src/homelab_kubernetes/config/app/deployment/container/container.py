import pulumi_kubernetes as kubernetes
from homelab_model import BaseModel

from . import image, port, resources, security_context


class Config(BaseModel):
    image: image.Config
    env: dict[str, str]
    ports: dict[str, port.Config]
    resources: resources.Config
    security_context: security_context.Config

    def to_args(self, name: str) -> kubernetes.core.v1.ContainerArgs:
        return kubernetes.core.v1.ContainerArgs(
            name=name,
            image=self.image.image,
            env=[kubernetes.core.v1.EnvVarArgs(name=name, value=value) for name, value in self.env.items()],
            ports=[port.to_args(name) for name, port in self.ports.items()],
            resources=self.resources.to_args(),
            security_context=self.security_context.to_args(),
        )
