from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config as config_
from .. import custom_resource, namespace


class Network(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "network"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config_.app.network.Config,
        *,
        opts: ResourceOptions,
        namespace: namespace.Namespace,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._namespace = namespace

        self.build_policies()

        self.register_outputs({})

    def build_policies(self) -> None:
        self._policies = {
            name: custom_resource.CustomResource(
                self._context,
                name,
                config=config_.custom_resource.Config(
                    api_version="cilium.io/v2", kind="CiliumNetworkPolicy", spec=policy
                ),
                opts=self._child_opts,
                namespace=self._namespace,
            )
            for name, policy in self._config.policies.items()
        }
