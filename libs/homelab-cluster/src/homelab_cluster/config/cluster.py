import functools

import homelab_common as common
import homelab_host as host
import homelab_kubernetes as kubernetes
import homelab_pulumi as pulumi
from homelab_model import BaseModel


class Config(BaseModel):
    kubernetes: kubernetes.config.Config
    host: host.config.Config

    @functools.cached_property
    def name(self) -> str:
        return common.string.add_prefix(
            pulumi.constant.STACK,
            common.string.add_prefix(
                self.kubernetes.domain.prefix,
                self.kubernetes.domain.name,
                separator=".",
            ),
            separator=".",
        )

    @functools.cached_property
    def endpoint(self) -> str:
        return f"https://{self.name}:6443"
