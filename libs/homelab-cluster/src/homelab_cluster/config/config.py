import functools

import homelab_common as common
import homelab_pulumi as pulumi
from homelab_types import BaseModel

from . import domain, host, version


class Config(BaseModel):
    name: str
    domain: domain.Config
    version: version.Config
    host: host.Config

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
