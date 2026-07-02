import homelab_pulumi as pulumi
import pulumi_kubernetes as kubernetes
from pulumi import ResourceOptions

from . import common


class Namespace:
    def __init__(self, name: str, *, opts: ResourceOptions) -> None:
        self._name = name
        self._namespace = kubernetes.core.v1.Namespace(
            name,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(name=name),
            opts=opts.merge(ResourceOptions(delete_before_replace=True)),
        )
        self.name = common.metadata.name(self._namespace.metadata)
        pulumi.data.export(f"kubernetes.namespace.{name}", self.name)
