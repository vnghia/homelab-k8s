from typing import ClassVar

from pulumi import ComponentResource, ResourceOptions

from .config import ClusterConfig
from .host import Host
from .secrets import ClusterSecrets


class Cluster(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cluster"

    def __init__(self, config: ClusterConfig, *, opts: ResourceOptions | None) -> None:
        super().__init__(self.RESOURCE_TYPE, config.name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._name = config.name
        self._config = config
        self._endpoint = (
            f"https://{self._config.hosts[self._config.endpoint].address}:6443"
        )
        self._secret = ClusterSecrets(
            opts=self._child_opts, version=self._config.version
        )

        self._hosts = {
            name: Host(
                name,
                config,
                opts=self._child_opts,
                cluser_name=self._name,
                cluser_version=self._config.version,
                cluser_endpoint=self._endpoint,
                cluser_secrets=self._secret,
            )
            for name, config in self._config.hosts.items()
        }

        self.register_outputs({})
