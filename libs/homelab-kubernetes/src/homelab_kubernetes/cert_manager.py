from typing import ClassVar

import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import config


class CertManager(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "cert-manager"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.cert_manager.Config,
        *,
        opts: ResourceOptions | None,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self._namespace = kubernetes.core.v1.Namespace(
            self._config.namespace,
            opts=self._child_opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(name=self._config.namespace),
        )
        self._chart = kubernetes.helm.v4.Chart(
            self._config.namespace,
            opts=self._child_opts.merge(ResourceOptions(depends_on=[self._namespace])),
            namespace=self._config.namespace,
            chart=self._config.chart,
            version=self._config.version,
            skip_crds=False,
            values={"crds": {"enabled": True}},
        )
