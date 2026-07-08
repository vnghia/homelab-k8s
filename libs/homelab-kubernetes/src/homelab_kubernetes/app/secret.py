import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from .. import common, config, namespace


class Secret:
    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.secret.Config,
        *,
        opts: ResourceOptions,
        namespace: namespace.Namespace,
    ) -> None:
        self._name = name
        self._context = context
        self._config = config
        self._namespace = namespace

        self._secret = kubernetes.core.v1.Secret(
            self._name,
            opts=opts,
            immutable=True,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(namespace=self._namespace.name),
            type=self._config.type,
            string_data=self._config.string_data.model_dump(
                context=self._context.to_serialization_context()
            ),
        )

        self.name = common.metadata.name(self._secret.metadata)
