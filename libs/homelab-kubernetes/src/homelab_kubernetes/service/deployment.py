from typing import ClassVar

import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config, namespace
from . import account


class Deployment(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "deployment"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.service.deployment.Config,
        *,
        opts: ResourceOptions,
        service: str,
        namespace: namespace.Namespace,
        service_accounts: dict[str, account.Account],
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._service = service
        self._namespace = namespace
        self._service_accounts = service_accounts

        self._labels = {"service": self._service, "app": self._name}
        self._deployment = kubernetes.apps.v1.Deployment(
            self._name,
            opts=self._child_opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                labels=self._labels, namespace=self._namespace.name
            ),
            spec=kubernetes.apps.v1.DeploymentSpecArgs(
                selector=kubernetes.meta.v1.LabelSelectorArgs(
                    match_labels=self._labels
                ),
                template=kubernetes.core.v1.PodTemplateSpecArgs(
                    metadata=kubernetes.meta.v1.ObjectMetaArgs(labels=self._labels),
                    spec=kubernetes.core.v1.PodSpecArgs(
                        service_account_name=self._service_accounts[
                            self._config.account
                        ].name
                        if self._config.account
                        else None,
                        containers=[
                            kubernetes.core.v1.ContainerArgs(
                                name=name,
                                image=container.image.image,
                                env=[
                                    kubernetes.core.v1.EnvVarArgs(
                                        name=name, value=value
                                    )
                                    for name, value in container.env.items()
                                ],
                            )
                            for name, container in self._config.containers.items()
                        ],
                    ),
                ),
            ),
        )
