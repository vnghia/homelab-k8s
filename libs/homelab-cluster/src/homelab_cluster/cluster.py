from typing import ClassVar

from pulumi import ComponentResource, ResourceOptions

from homelab_cluster.image import Image

from .config import ClusterConfig
from .host import Host
from .secrets import ClusterSecrets


class Cluster(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cluster"

    def __init__(self, config: ClusterConfig, *, opts: ResourceOptions | None) -> None:
        super().__init__(self.RESOURCE_TYPE, config.name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config
        self._secret = ClusterSecrets(
            opts=self._child_opts, version=self._config.version
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
                cluser_secrets=self._secret,
            )
            for name, config in self._config.hosts.items()
        }

        self.register_outputs({})
