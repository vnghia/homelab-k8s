from typing import Self

import homelab_cluster as cluster
import homelab_common as common
import homelab_context as context
import homelab_dns as dns
from homelab_model import BaseModel
from nickel import nickel


class Config(BaseModel):
    dns: dns.config.Config
    cluster: cluster.config.Config

    @classmethod
    def load(cls, context: context.Context) -> Self:
        nickel_config = (
            (common.constant.path.ROOT / "config" / "homelab.ncl")
            .resolve(True)
            .as_posix()
        )
        return cls.model_validate_json(
            nickel.run(
                f'(import "{nickel_config}") & (std.deserialize \'Json (m%%%"{context.pulumi.require("config")}"%%%))'
            )
        )
