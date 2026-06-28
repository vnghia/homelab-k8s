from typing import ClassVar

import homelab_kubernetes as kubernetes
from pulumi import ComponentResource, ResourceOptions

from .. import config
from ..secrets import Secrets
from .image import Image
from .machine import Machine


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        name: str,
        config: config.host.Config,
        *,
        opts: ResourceOptions | None,
        kubernetes_config: kubernetes.config.Config,
        cluster_name: str,
        cluster_endpoint: str,
        cluster_secrets: Secrets,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config
        self._kubernetes_config = kubernetes_config
        self._cluster_name = cluster_name
        self._cluster_endpoint = cluster_endpoint
        self._cluster_secrets = cluster_secrets

        self.build_images()
        self.build_machines()

    def build_images(self) -> None:
        self._images = {
            name: Image(name, config, opts=self._child_opts, host_config=self._config)
            for name, config in self._config.images.items()
        }

    def build_machines(self) -> None:
        self._machines = {
            name: Machine(
                name,
                config,
                opts=self._child_opts,
                host_config=self._config,
                host_images=self._images,
                kubernetes_config=self._kubernetes_config,
                cluster_name=self._cluster_name,
                cluster_endpoint=self._cluster_endpoint,
                cluster_secrets=self._cluster_secrets,
            )
            for name, config in self._config.machines.items()
        }

        self.bootstrap = self._machines[self._config.bootstrap]

        self.controlplane_endpoints = [
            machine._endpoint
            for machine in self._machines.values()
            if machine._config.features.controlplane
        ]
        self.machine_endpoints = [
            machine._endpoint for machine in self._machines.values()
        ]
