from typing import ClassVar

import homelab_dns as dns
import homelab_host as host
import homelab_kubernetes as kubernetes
import homelab_pulumi as pulumi
import pulumi_kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import config


class Cluster(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cluster"

    def __init__(
        self,
        context: Context,
        config: config.Config,
        *,
        opts: ResourceOptions | None,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, config.name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._dns = dns

        self.build_host()

        pulumi.data.export("cluster.talosconfig", self._host.talosconfig)
        pulumi.data.export("cluster.kubeconfig", self._host.kubeconfig)

        self.build_kubernetes()

        self.register_outputs({})

    def build_host(self) -> None:
        self._host = host.Host(
            self._context,
            self._config.name,
            self._config.host,
            opts=self._child_opts,
            kubernetes_config=self._config.kubernetes,
            cluster_name=self._name,
            cluster_endpoint=self._config.endpoint,
        )

    def build_kubernetes(self) -> None:
        self._kubernetes = kubernetes.Kubernetes(
            self._context,
            self._config.name,
            config=self._config.kubernetes,
            opts=self._child_opts.merge(
                ResourceOptions(
                    providers={
                        "kubernetes": pulumi_kubernetes.Provider(
                            self._name,
                            kubeconfig=self._host.kubeconfig,
                        ),
                    },
                ),
            ),
        )
