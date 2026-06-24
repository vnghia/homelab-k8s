from typing import ClassVar

import pulumiverse_talos as talos
from pulumi import ComponentResource, ResourceOptions

from .config import HostConfig


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self, name: str, config: HostConfig, *, opts: ResourceOptions | None
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)

        self._child_opts = ResourceOptions(parent=self)
        self._name = name
        self._config = config

        self._extensions = talos.imagefactory.get_extensions_versions_output(
            talos_version=self._config.image.version,
            filters=talos.imagefactory.GetExtensionsVersionsFiltersArgs(
                names=self._config.image.extensions
            ),
        )

        self.register_outputs({})
