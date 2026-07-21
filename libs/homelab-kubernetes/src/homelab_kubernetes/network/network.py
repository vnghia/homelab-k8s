import typing
from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config, custom_resource
from . import certificate, gateways

if typing.TYPE_CHECKING:
    from .. import app


class network(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "network"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.network.Config,
        *,
        opts: ResourceOptions,
        data: app.reference.Data,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self._reference_app_data = data

        self.build_certificate()
        self.build_gateways()
        self.build_policies()

        self.register_outputs({})

    def build_certificate(self) -> None:
        self._certificate = certificate.Certificate(
            self._context, self._config.certificate, opts=self._child_opts, data=self._reference_app_data
        )

    def build_gateways(self) -> None:
        self._gateways = gateways.Gateways(self._context, self._name, self._config.gateway, opts=self._child_opts)

    def build_policies(self) -> None:
        self._policies = {
            name: custom_resource.CustomResource(
                self._context,
                name,
                config=config.custom_resource.Config(
                    api_version="cilium.io/v2", kind="CiliumClusterwideNetworkPolicy", spec=policy
                ),
                opts=self._child_opts,
                namespace=None,
            )
            for name, policy in self._config.policies.items()
        }
