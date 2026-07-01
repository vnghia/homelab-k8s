from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import config


class Kubernetes(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "kubernetes"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.Config,
        *,
        opts: ResourceOptions,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)
