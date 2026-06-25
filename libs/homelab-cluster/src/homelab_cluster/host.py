from typing import ClassVar

from pulumi import ComponentResource, ResourceOptions

from homelab_cluster.secrets import ClusterSecrets

from .config import ClusterConfig, HostConfig


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        name: str,
        config: HostConfig,
        *,
        opts: ResourceOptions | None,
        cluster_config: ClusterConfig,
        cluser_secrets: ClusterSecrets,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._name = name
        self._config = config
