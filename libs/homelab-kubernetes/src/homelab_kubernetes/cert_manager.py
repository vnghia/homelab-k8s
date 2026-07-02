from typing import ClassVar

import homelab_dns as dns
import homelab_pulumi
import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import common, config, namespace


class CertManager(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cert-manager"

    API_TOKEN_KEY: ClassVar[str] = "api-token"  # noqa: S105

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.cert_manager.Config,
        *,
        opts: ResourceOptions,
        dns: dns.Dns,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._dns = dns

        self._namespace = namespace.Namespace(
            self._config.namespace, opts=self._child_opts
        )

        self._manager = kubernetes.helm.v4.Chart(
            self._config.namespace,
            opts=self._child_opts,
            namespace=self._namespace.name,
            chart=self._config.chart,
            version=self._config.version,
            skip_crds=False,
            values={"crds": {"enabled": True}, "config": {"enableGatewayAPI": True}},
        )

        self._issuer_token = kubernetes.core.v1.Secret(
            f"{self._config.issuer}-token",
            opts=self._child_opts,
            immutable=True,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(namespace=self._namespace.name),
            type="Opaque",
            string_data={self.API_TOKEN_KEY: self._dns.token.cert_manager},
        )

        self._issuer = kubernetes.apiextensions.CustomResource(
            self._config.issuer,
            opts=self._child_opts.merge(ResourceOptions(depends_on=[self._manager])),
            api_version="cert-manager.io/v1",
            kind="ClusterIssuer",
            spec={
                "acme": {
                    "server": "https://acme-staging-v02.api.letsencrypt.org/directory"
                    if homelab_pulumi.constant.STACK
                    else "https://acme-v02.api.letsencrypt.org/directory",
                    "email": self._config.email,
                    "privateKeySecretRef": {
                        "name": f"{self._config.issuer}-account-key"
                    },
                    "solvers": [
                        {
                            "dns01": {
                                "cloudflare": {
                                    "apiTokenSecretRef": {
                                        "name": common.metadata.name(
                                            self._issuer_token.metadata
                                        ),
                                        "key": self.API_TOKEN_KEY,
                                    }
                                }
                            }
                        }
                    ],
                }
            },
        )
