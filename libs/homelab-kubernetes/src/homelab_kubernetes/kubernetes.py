from typing import ClassVar

import homelab_dns as dns
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import app, cert_manager, config, gateways


class Kubernetes(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "kubernetes"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.Config,
        *,
        opts: ResourceOptions,
        dns: dns.Dns,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self, delete_before_replace=True)

        self._context = context
        self._config = config
        self._dns = dns

        self.build_cert_manager()
        self.build_gateways()
        self.build_apps()

    def build_cert_manager(self) -> None:
        self._cert_manager = cert_manager.CertManager(
            self._context,
            self._config.apps.cert_manager,
            opts=self._child_opts,
            dns=self._dns,
        )

    def build_gateways(self) -> None:
        self._gateways = gateways.Gateways(
            self._context,
            self._name,
            self._config.networking.gateway,
            opts=self._child_opts,
        )

    def build_apps(self) -> None:
        self._apps = {
            name: app.App(self._context, name, config, opts=self._child_opts)
            for name, config in self._config.apps.apps.items()
        }
