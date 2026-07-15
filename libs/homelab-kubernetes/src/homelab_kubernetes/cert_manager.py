from typing import ClassVar

import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from . import app, config


class CertManager(app.App[config.cert_manager.Config]):
    API_TOKEN_KEY: ClassVar[str] = "api-token"  # noqa: S105

    def __init__(self, context: Context, config: config.cert_manager.Config, *, opts: ResourceOptions) -> None:
        super().__init__(context, config.namespace.name, config, opts=opts, register_output=False)

        self._manager = kubernetes.helm.v4.Chart(
            self._config.namespace.name,
            opts=self._child_opts,
            namespace=self._namespace.name,
            chart=self._config.chart,
            version=self._config.version,
            skip_crds=False,
            values={
                "crds": {"enabled": True},
                "config": {
                    "enableGatewayAPI": True,
                    "enableGatewayAPIListenerSet": True,
                    "featureGates": {"ListenerSets": True},
                },
            },
        )

        self.register_outputs({})
