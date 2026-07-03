import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ResourceOptions

from .. import config, namespace
from . import deployment


class Service:
    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.service.Config,
        *,
        opts: ResourceOptions,
        app: str,
        namespace: namespace.Namespace,
        deployments: dict[str, deployment.Deployment],
    ) -> None:
        self._child_opts = opts

        self._name = name
        self._context = context
        self._config = config
        self._app = app
        self._namespace = namespace
        self._deployment = deployments[self._config.deployment]

        self._service = kubernetes.core.v1.Service(
            self._name,
            opts=self._child_opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                namespace=self._namespace.name, labels=self._deployment.labels
            ),
            spec=kubernetes.core.v1.ServiceSpecArgs(
                ports=[
                    kubernetes.core.v1.ServicePortArgs(
                        name=name,
                        port=port.port or target_port,
                        target_port=target_port,
                    )
                    for name, port in self._config.ports.items()
                    if (
                        container := self._deployment._config.containers[
                            port.container.container
                        ]
                    )
                    and (
                        target_port := container.ports[
                            port.container.port
                        ].container_port
                    )
                ],
                selector=self._deployment.labels,
            ),
        )
