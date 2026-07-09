from typing import ClassVar

import homelab_pulumi as pulumi
import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import common, namespace
from .. import config as config_
from . import account


class Deployment(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "deployment"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config_.app.deployment.Config,
        *,
        opts: ResourceOptions,
        app: str,
        namespace: namespace.Namespace,
        accounts: dict[str, account.Account],
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._app = app
        self._namespace = namespace
        self._accounts = accounts

        self.labels = self._namespace.build_labels(apps={"component": self._name})

        self._deployment = kubernetes.apps.v1.Deployment(
            self._name,
            opts=self._child_opts,
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                labels=self.labels,
                namespace=self._namespace.name,
            ),
            spec=kubernetes.apps.v1.DeploymentSpecArgs(
                selector=kubernetes.meta.v1.LabelSelectorArgs(match_labels=self.labels),
                template=kubernetes.core.v1.PodTemplateSpecArgs(
                    metadata=kubernetes.meta.v1.ObjectMetaArgs(labels=self.labels),
                    spec=kubernetes.core.v1.PodSpecArgs(
                        service_account_name=self._accounts[self._config.account].name
                        if self._config.account
                        else None,
                        resources=self._config.resources.to_args(),
                        security_context=self._config.security_context.to_args(),
                        containers=[
                            container.to_args(name)
                            for name, container in self._config.containers.items()
                        ],
                    ),
                ),
            ),
        )

        pulumi.data.export(
            f"deployment.{self._app}.{self._name}",
            common.metadata.name(self._deployment.metadata),
        )
        self.register_outputs({})

    @property
    def config(self) -> config_.app.deployment.Config:
        return self._config
