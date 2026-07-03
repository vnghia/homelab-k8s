import homelab_pulumi as pulumi
import pulumi_kubernetes as kubernetes
from pulumi import ResourceOptions

from . import common, config


class Namespace:
    def __init__(
        self, name: str, config: config.namespace.Config, *, opts: ResourceOptions
    ) -> None:
        self._name = name
        self._namespace = kubernetes.core.v1.Namespace(
            name,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                name=name, labels=config.to_labels()
            ),
            opts=opts.merge(ResourceOptions(delete_before_replace=True)),
        )
        self.name = common.metadata.name(self._namespace.metadata)
        pulumi.data.export(f"kubernetes.namespace.{name}", self.name)
