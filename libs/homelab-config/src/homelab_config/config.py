import tempfile
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
        with tempfile.NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".json"
        ) as homelab_config:
            homelab_config.write(context.pulumi.require("config"))
            homelab_config.flush()

            nickel_config = (
                (common.constant.path.ROOT / "config" / "homelab.ncl")
                .resolve(True)
                .as_posix()
            )

            return cls.model_validate_json(
                nickel.run(
                    " & ".join(
                        [
                            f'(import "{path}")'
                            for path in [homelab_config.name, nickel_config]
                        ]
                    )
                )
            )
