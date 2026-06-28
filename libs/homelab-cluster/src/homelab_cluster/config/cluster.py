import functools

import homelab_common as common
import homelab_kubernetes as kubernetes
import homelab_pulumi as pulumi
from homelab_types import BaseModel

from . import host


class Config(BaseModel):
    name: str
    kubernetes: kubernetes.config.Config
    host: host.Config

    @functools.cached_property
    def endpoint(self) -> str:
        return f"https://{
            common.string.add_prefix(
                pulumi.constant.STACK,
                common.string.add_prefix(
                    self.kubernetes.domain.prefix,
                    self.kubernetes.domain.name,
                    separator='.',
                ),
                separator='.',
            )
        }:6443"
