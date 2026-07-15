from typing import Self

import homelab_cluster as cluster
import homelab_common as common
import homelab_dns as dns
import homelab_pulumi as pulumi
from homelab_model import BaseModel
from nickel import nickel


class Config(BaseModel):
    dns: dns.config.Config
    cluster: cluster.config.Config

    @classmethod
    def load(cls, data: pulumi.reference.Data) -> Self:
        nickel_config = (common.constant.path.ROOT / "config" / "homelab.ncl").resolve(True).as_posix()
        return cls.model_validate_json(
            nickel.run(
                f'(import "{nickel_config}") & '
                f'(std.deserialize \'Json (m%%%"{data.config}"%%%)) & '
                f"{{ cluster.stack = {('"' + pulumi.constant.STACK + '"') if pulumi.constant.STACK else 'null'} }}"
            )
        )
