import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from . import common, config, namespace


class CustomResource:
    def __init__(
        self,
        context: Context,
        name: str,
        config: config.custom_resource.Config,
        *,
        opts: ResourceOptions,
        namespace: namespace.Namespace | None,
    ) -> None:
        self._name = name
        self._context = context
        self._config = config
        self._namespace = namespace

        self._resource = kubernetes.apiextensions.CustomResource(
            self._name,
            opts=opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(namespace=self._namespace.name) if self._namespace else None,
            api_version=self._config.api_version,
            kind=self._config.kind,
            spec=self._config.spec.model_dump(context=self._context.asdict()),
        )

        self.name = common.metadata.name(self._resource.__dict__["metadata"])

    @property
    def resource(self) -> kubernetes.apiextensions.CustomResource:
        return self._resource
