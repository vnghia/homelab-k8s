from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import app, config, network


class Kubernetes(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "kubernetes"

    def __init__(self, context: Context, name: str, config: config.Config, *, opts: ResourceOptions) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self, delete_before_replace=True)

        self._context = context
        self._config = config

        self._reference_app_data = app.reference.Data(apps={})
        self._context.set(app.reference.Reference, self._reference_app_data)

        self.build_network()
        self.build_apps()

        self.register_outputs({})

    def build_network(self) -> None:
        self._network = network.network(
            self._context, self._name, self._config.network, opts=self._child_opts, data=self._reference_app_data
        )

    def build_apps(self) -> None:
        self._apps = {
            name: app.App(self._context, name, config, opts=self._child_opts, data=self._reference_app_data)
            for name, config in self._config.apps.items()
        }
