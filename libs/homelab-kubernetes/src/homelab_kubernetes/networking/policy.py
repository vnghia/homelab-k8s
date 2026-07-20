from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config, custom_resource


class Policy(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "policy"

    def __init__(
        self, context: Context, name: str, config: config.networking.policy.Config, *, opts: ResourceOptions
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self.build_cluster()

        self.register_outputs({})

    def build_cluster(self) -> None:
        self._cluster = {
            name: custom_resource.CustomResource(
                self._context,
                name,
                config=config.custom_resource.Config(
                    api_version="cilium.io/v2", kind="CiliumClusterwideNetworkPolicy", spec=spec
                ),
                opts=self._child_opts,
                namespace=None,
            )
            for name, spec in self._config.cluster.items()
        }
