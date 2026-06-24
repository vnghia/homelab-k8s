from typing import ClassVar

import pulumi
import pulumiverse_talos as talos
from homelab_pulumi.data import OutputSerializer
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

        self._schematic = talos.imagefactory.Schematic(
            self._name,
            opts=self._child_opts,
            schematic=OutputSerializer.yaml(
                {
                    "customization": {
                        "systemExtensions": {
                            "officialExtensions": self._extensions.apply(
                                lambda result: [
                                    info.name for info in result.extensions_infos
                                ]
                            )
                        }
                    }
                }
            ),
        )

        pulumi.export(f"host.{self._name}.image.schematic", self._schematic.id)

        self.register_outputs({})
