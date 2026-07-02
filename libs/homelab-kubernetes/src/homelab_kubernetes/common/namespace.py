import homelab_pulumi as pulumi
import pulumi_kubernetes as kubernetes
from pulumi import Output, ResourceOptions

from . import metadata


def create(
    name: str, opts: ResourceOptions
) -> tuple[kubernetes.core.v1.Namespace, Output[str]]:
    namespace = kubernetes.core.v1.Namespace(
        name,
        metadata=kubernetes.meta.v1.ObjectMetaArgs(name=name),
        opts=opts.merge(ResourceOptions(delete_before_replace=True)),
    )
    namespace_name = metadata.name(namespace.metadata)
    pulumi.data.export(f"kubernetes.namespace.{name}", namespace_name)
    return namespace, namespace_name
