from typing import ClassVar

import homelab_kubernetes as kubernetes
import pulumiverse_talos as talos
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import config
from .image import Image
from .machine import Machine
from .secrets import Secrets


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.Config,
        *,
        opts: ResourceOptions | None,
        kubernetes_config: kubernetes.config.Config,
        cluster_name: str,
        cluster_endpoint: str,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._kubernetes_config = kubernetes_config
        self._cluster_name = cluster_name
        self._cluster_endpoint = cluster_endpoint

        self._secrets = Secrets(opts=self._child_opts, version=self._config.version)

        self.build_images()
        self.build_machines()
        self.build_config()

        self.register_outputs({})

    def build_images(self) -> None:
        self._images = {
            name: Image(
                self._context,
                name,
                config,
                opts=self._child_opts,
                host_config=self._config,
            )
            for name, config in self._config.images.items()
        }

    def build_machines(self) -> None:
        self._machines = {
            name: Machine(
                self._context,
                name,
                config,
                opts=self._child_opts,
                host_config=self._config,
                host_images=self._images,
                host_secrets=self._secrets,
                kubernetes_config=self._kubernetes_config,
                cluster_name=self._cluster_name,
                cluster_endpoint=self._cluster_endpoint,
            )
            for name, config in self._config.machines.items()
        }

        self.bootstrap = self._machines[self._config.bootstrap]

        self.controlplane_endpoints = [
            machine.endpoint
            for machine in self._machines.values()
            if machine.features.controlplane
        ]
        self.machine_endpoints = [
            machine.endpoint for machine in self._machines.values()
        ]

    def build_config(self) -> None:
        self.kubeconfig = talos.cluster.Kubeconfig(
            self._name,
            opts=self._child_opts.merge(
                ResourceOptions(depends_on=self.bootstrap.machine_bootstrap),
            ),
            client_configuration=self._secrets.client_configuration_output.apply(
                lambda client_configuration: (
                    talos.cluster.KubeconfigClientConfigurationArgs(
                        ca_certificate=client_configuration.ca_certificate,
                        client_certificate=client_configuration.client_certificate,
                        client_key=client_configuration.client_key,
                    )
                ),
            ),
            node=self.bootstrap.endpoint,
        ).kubeconfig_raw

        self.talosconfig = talos.client.get_configuration_output(
            client_configuration=self._secrets.client_configuration_output.apply(
                lambda client_configuration: (
                    talos.client.GetConfigurationClientConfigurationArgs(
                        ca_certificate=client_configuration.ca_certificate,
                        client_certificate=client_configuration.client_certificate,
                        client_key=client_configuration.client_key,
                    )
                ),
            ),
            cluster_name=self._name,
            endpoints=self.controlplane_endpoints,
            nodes=self.machine_endpoints,
        ).apply(lambda result: result.talos_config)
