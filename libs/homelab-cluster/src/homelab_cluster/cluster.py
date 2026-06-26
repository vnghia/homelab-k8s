from typing import ClassVar

import pulumi
import pulumiverse_talos as talos
from pulumi import ComponentResource, ResourceOptions

from homelab_cluster.image import Image

from .config import ClusterConfig
from .host import Host
from .secrets import Secrets


class Cluster(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cluster"

    def __init__(self, config: ClusterConfig, *, opts: ResourceOptions | None) -> None:
        super().__init__(self.RESOURCE_TYPE, config.name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config
        self._secrets = Secrets(
            opts=self._child_opts, version=self._config.version.talos
        )

        self._images = {
            name: Image(
                name, config, opts=self._child_opts, cluster_config=self._config
            )
            for name, config in self._config.images.items()
        }

        self._hosts = {
            name: Host(
                name,
                config,
                opts=self._child_opts,
                cluster_config=self._config,
                cluster_secrets=self._secrets,
                cluster_images=self._images,
            )
            for name, config in self._config.hosts.items()
        }
        self._host_bootstrap = self._hosts[self._config.bootstrap]

        self._controlplane_endpoints = [
            host._endpoint
            for host in self._hosts.values()
            if host._config.features.controlplane
        ]
        self._host_endpoints = [host._endpoint for host in self._hosts.values()]

        self._cluster_kubeconfig = talos.cluster.Kubeconfig(
            self._name,
            opts=self._child_opts.merge(
                ResourceOptions(depends_on=self._host_bootstrap._machine_bootstrap)
            ),
            client_configuration=self._secrets.client_configuration_output.apply(
                lambda client_configuration: (
                    talos.cluster.KubeconfigClientConfigurationArgs(
                        ca_certificate=client_configuration.ca_certificate,
                        client_certificate=client_configuration.client_certificate,
                        client_key=client_configuration.client_key,
                    )
                )
            ),
            node=self._hosts[self._config.bootstrap]._endpoint,
        )

        pulumi.export(
            "cluster.talosconfig",
            talos.client.get_configuration_output(
                client_configuration=self._secrets.client_configuration_output.apply(
                    lambda client_configuration: (
                        talos.client.GetConfigurationClientConfigurationArgs(
                            ca_certificate=client_configuration.ca_certificate,
                            client_certificate=client_configuration.client_certificate,
                            client_key=client_configuration.client_key,
                        )
                    )
                ),
                cluster_name=self._name,
                endpoints=self._controlplane_endpoints,
                nodes=self._host_endpoints,
            ).apply(lambda result: result.talos_config),
        )
        pulumi.export("cluster.kubeconfig", self._cluster_kubeconfig.kubeconfig_raw)

        self.register_outputs({})
