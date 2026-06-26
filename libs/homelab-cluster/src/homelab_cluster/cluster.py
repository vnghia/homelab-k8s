from typing import ClassVar

import homelab_pulumi as pulumi
import pulumiverse_talos as talos
from pulumi import ComponentResource, ResourceOptions

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
        self.build_host()

        self.build_config()
        pulumi.data.export("cluster.talosconfig", self._talosconfig)
        pulumi.data.export("cluster.kubeconfig", self._kubeconfig)

        self.register_outputs({})

    def build_secrets(self) -> None:
        self._secrets = Secrets(
            opts=self._child_opts, version=self._config.version.talos
        )

    def build_host(self) -> None:
        self._host = Host(
            self._config.name,
            self._config.host,
            opts=self._child_opts,
            cluster_config=self._config,
            cluster_secrets=self._secrets,
        )

    def build_config(self) -> None:
        self._kubeconfig = talos.cluster.Kubeconfig(
            self._name,
            opts=self._child_opts.merge(
                ResourceOptions(depends_on=self._host.bootstrap._machine_bootstrap)
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
            node=self._host.bootstrap._endpoint,
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
            endpoints=self._host.controlplane_endpoints,
            nodes=self._host.machine_endpoints,
        ).apply(lambda result: result.talos_config)
