import typing
from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config
from . import certificate, gateways, policy

if typing.TYPE_CHECKING:
    from .. import app


class Networking(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "networking"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.networking.Config,
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
        self.build_policy()

        self.register_outputs({})

    def build_certificate(self) -> None:
        self._certificate = certificate.Certificate(
            self._context, self._config.certificate, opts=self._child_opts, data=self._reference_app_data
        )

    def build_gateways(self) -> None:
        self._gateways = gateways.Gateways(self._context, self._name, self._config.gateway, opts=self._child_opts)

    def build_policy(self) -> None:
        self._policy = policy.Policy(self._context, self._name, config=self._config.policy, opts=self._child_opts)
