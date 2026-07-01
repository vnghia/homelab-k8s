from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import cert_manager, config


class Kubernetes(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "kubernetes"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.Config,
        *,
        opts: ResourceOptions,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self.build_cert_manager()

    def build_cert_manager(self) -> None:
        self._cert_manager = cert_manager.CertManager(
            self._context, self._name, self._config.cert_manager, opts=self._child_opts
        )
