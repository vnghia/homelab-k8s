import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from .. import common, config, namespace


class CustomResource:
    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.custom_resource.Config,
        *,
        opts: ResourceOptions,
        namespace: namespace.Namespace,
    ) -> None:
        self._name = name
        self._context = context
        self._config = config
        self._namespace = namespace

        self._resource = kubernetes.apiextensions.CustomResource(
            self._name,
            opts=opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(namespace=self._namespace.name),
            api_version=self._config.api_version,
            kind=self._config.kind,
            spec=self._config.spec.model_dump(
                context=self._context.to_serialization_context()
            ),
        )

        self.name = common.metadata.name(self._resource.__dict__["metadata"])
