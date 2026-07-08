from typing import ClassVar

import homelab_dns as dns
import homelab_host as host
import homelab_kubernetes as kubernetes
import homelab_pulumi as pulumi
import pulumi_kubernetes
import pulumiverse_talos as talos
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

        self.build_config()
        pulumi.data.export("cluster.talosconfig", self._talosconfig)
        pulumi.data.export("cluster.kubeconfig", self._kubeconfig)

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

    def build_config(self) -> None:
        self._kubeconfig = talos.cluster.Kubeconfig(
            self._name,
            opts=self._child_opts.merge(
                ResourceOptions(depends_on=self._host.bootstrap._machine_bootstrap)
            ),
            client_configuration=self._host._secrets.client_configuration_output.apply(
                lambda client_configuration: (
                    talos.cluster.KubeconfigClientConfigurationArgs(
                        ca_certificate=client_configuration.ca_certificate,
                        client_certificate=client_configuration.client_certificate,
                        client_key=client_configuration.client_key,
                    )
                )
            ),
            node=self._host.bootstrap._endpoint,
        ).kubeconfig_raw

        self._talosconfig = talos.client.get_configuration_output(
            client_configuration=self._host._secrets.client_configuration_output.apply(
                lambda client_configuration: (
                    talos.client.GetConfigurationClientConfigurationArgs(
                        ca_certificate=client_configuration.ca_certificate,
                        client_certificate=client_configuration.client_certificate,
                        client_key=client_configuration.client_key,
                    )
                )
            ),
            cluster_name=self._name,
            endpoints=self._host.controlplane_endpoints,
            nodes=self._host.machine_endpoints,
        ).apply(lambda result: result.talos_config)

    def build_kubernetes(self) -> None:
        self._kubernetes = kubernetes.Kubernetes(
            self._context,
            self._config.name,
            config=self._config.kubernetes,
            opts=self._child_opts.merge(
                ResourceOptions(
                    providers={
                        "kubernetes": pulumi_kubernetes.Provider(
                            self._name, kubeconfig=self._kubeconfig
                        )
                    }
                ),
            ),
        )
