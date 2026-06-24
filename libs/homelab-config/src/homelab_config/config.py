import tempfile
from typing import Self

import pulumi
from homelab_common import constant
from homelab_host.config import HostsConfig
from homelab_types import BaseModel
from nickel import nickel


class Config(BaseModel):
    hosts: HostsConfig

    @classmethod
    def load(cls) -> Self:
        pulumi_config = pulumi.Config()

        with tempfile.NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".json"
        ) as homelab_config:
            homelab_config.write(pulumi_config.require("config"))
            homelab_config.flush()

            nickel_config = (
                (constant.path.ROOT / "config" / "homelab.ncl").resolve(True).as_posix()
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
