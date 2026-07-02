from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from .. import common, config


class Service(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "service"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.service.Config,
        *,
        opts: ResourceOptions,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._namespace, self._namespace_name = common.namespace.create(
            f"service-{self._name}", self._child_opts
        )

        self.register_outputs({})
