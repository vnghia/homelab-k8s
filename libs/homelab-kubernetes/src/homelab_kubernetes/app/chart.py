import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from .. import config, namespace


class Chart:
    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.chart.Config,
        *,
        opts: ResourceOptions,
        namespace: namespace.Namespace,
    ) -> None:
        self._name = name
        self._context = context
        self._config = config
        self._namespace = namespace

        self._chart = kubernetes.helm.v4.Chart(
            self._name,
            opts=opts,
            namespace=self._namespace.name,
            chart=self._config.chart,
            version=self._config.version,
            skip_crds=self._config.skip_crds,
            values=self._config.values.model_dump(context=self._context.asdict()),
        )

    @property
    def chart(self) -> kubernetes.helm.v4.Chart:
        return self._chart
