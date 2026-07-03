from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config, namespace
from . import account, deployment


class App(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "app"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.app.Config,
        *,
        opts: ResourceOptions,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self.build_namespace()
        self.build_accounts()
        self.build_deployments()

        self.register_outputs({})

    def build_namespace(self) -> None:
        self._namespace = namespace.Namespace(
            self._config.namespace.name or self._name,
            self._config.namespace.config,
            opts=self._child_opts,
        )

    def build_accounts(self) -> None:
        self._accounts = {
            name: account.Account(
                self._context,
                name,
                config,
                opts=self._child_opts,
                app=self._name,
                namespace=self._namespace,
            )
            for name, config in self._config.accounts.items()
        }

    def build_deployments(self) -> None:
        self._deployments = {
            name: deployment.Deployment(
                self._context,
                name,
                config,
                opts=self._child_opts,
                app=self._name,
                namespace=self._namespace,
                accounts=self._accounts,
            )
            for name, config in self._config.deployments.items()
        }
