import functools

import homelab_common as common
import homelab_pulumi as pulumi
from homelab_types import BaseModel

from . import host, image, version


class DomainConfig(BaseModel):
    prefix: str | None
    name: str


class Config(BaseModel):
    name: str
    bootstrap: str
    domain: DomainConfig
    version: version.Config
    images: dict[str, image.Config]
    hosts: dict[str, host.Config]

    @functools.cached_property
    def endpoint(self) -> str:
        return f"https://{
            common.string.add_prefix(
                pulumi.constant.STACK,
                common.string.add_prefix(
                    self.domain.prefix, self.domain.name, separator='.'
                ),
                separator='.',
            )
        }:6443"
