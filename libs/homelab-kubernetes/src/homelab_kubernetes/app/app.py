import typing
from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import config, namespace
from . import account, chart, custom_resource, deployment, secret, service
from . import context as context_

if typing.TYPE_CHECKING:
    from . import reference


class App[T: config.app.Config = config.app.Config](ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "app"

    def __init__(
        self,
        context: Context,
        name: str,
        config: T,
        *,
        opts: ResourceOptions,
        data: reference.Data,
        register_output: bool = True,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)
        data.apps[name] = self

        self._context = context_.Context(name=self._name, **context.asdict())
        self._config = config

        self.build_namespace()
        self.build_accounts()
        self.build_secrets()
        self.build_charts()
        self.build_custom_resources()
        self.build_deployments()
        self.build_services()

        if register_output:
            self.register_outputs({})

    @property
    def secrets(self) -> dict[str, secret.Secret]:
        return self._secrets

    def build_namespace(self) -> None:
        self._namespace = namespace.Namespace(
            self._config.namespace.model_copy(update={"name": self._config.namespace.name or self._name}),
            opts=self._child_opts,
        )

    def build_accounts(self) -> None:
        self._accounts = {
            name: account.Account(
                self._context, name, config, opts=self._child_opts, app=self._name, namespace=self._namespace
            )
            for name, config in self._config.accounts.items()
        }

    def build_secrets(self) -> None:
        self._secrets = {
            name: secret.Secret(self._context, name, config, opts=self._child_opts, namespace=self._namespace)
            for name, config in self._config.secrets.items()
        }

    def build_charts(self) -> None:
        self._charts = {
            name: chart.Chart(self._context, name, config, opts=self._child_opts, namespace=self._namespace)
            for name, config in self._config.charts.items()
        }

    def build_custom_resources(self) -> None:
        self._custom_resources = {
            name: custom_resource.CustomResource(
                self._context, name, config, opts=self._child_opts, namespace=self._namespace
            )
            for name, config in self._config.custom_resources.items()
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

    def build_services(self) -> None:
        self._services = {
            name: service.Service(
                self._context,
                name,
                config,
                opts=self._child_opts,
                app=self._name,
                namespace=self._namespace,
                deployments=self._deployments,
            )
            for name, config in self._config.services.items()
        }
