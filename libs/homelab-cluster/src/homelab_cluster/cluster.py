from typing import ClassVar

import homelab_pulumi as pulumi
import pulumiverse_talos as talos
from pulumi import ComponentResource, ResourceOptions

from homelab_cluster.image import Image

from . import config
from .host import Host
from .secrets import Secrets


class Cluster(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cluster"

    def __init__(self, config: config.Config, *, opts: ResourceOptions | None) -> None:
        super().__init__(self.RESOURCE_TYPE, config.name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config

        self.build_secrets()
        self.build_images()
        self._host_bootstrap = self.build_hosts()

        self.build_config()
        pulumi.data.export("cluster.talosconfig", self._talosconfig)
        pulumi.data.export("cluster.kubeconfig", self._kubeconfig)

        self.register_outputs({})

    def build_secrets(self) -> None:
        self._secrets = Secrets(
            opts=self._child_opts, version=self._config.version.talos
        )

    def build_images(self) -> None:
        self._images = {
            name: Image(
                name, config, opts=self._child_opts, cluster_config=self._config
            )
            for name, config in self._config.images.items()
        }

    def build_hosts(self) -> Host:
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
        return self._hosts[self._config.bootstrap]

    def build_config(self) -> None:
        controlplane_endpoints = [
            host._endpoint
            for host in self._hosts.values()
            if host._config.features.controlplane
        ]
        host_endpoints = [host._endpoint for host in self._hosts.values()]

        self._kubeconfig = talos.cluster.Kubeconfig(
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
        ).kubeconfig_raw

        self._talosconfig = talos.client.get_configuration_output(
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
            endpoints=controlplane_endpoints,
            nodes=host_endpoints,
        ).apply(lambda result: result.talos_config)
