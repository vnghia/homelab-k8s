from typing import ClassVar

import homelab_pulumi as pulumi
import pulumiverse_talos as talos
from pulumi import ComponentResource, Output, ResourceOptions

from . import config


class Image(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "image"

    def __init__(
        self,
        name: str,
        config: config.image.Config,
        *,
        opts: ResourceOptions | None,
        host_config: config.host.Config,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config

        self._extensions = talos.imagefactory.get_extensions_versions_output(
            talos_version=host_config.version,
            filters=talos.imagefactory.GetExtensionsVersionsFiltersArgs(
                names=self._config.extensions
            ),
        )

        self._schematic = talos.imagefactory.Schematic(
            self._name,
            opts=self._child_opts,
            schematic=pulumi.data.serialize.yaml(
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
                },
                False,
            ),
        )

        self.id = self._schematic.id
        self.url = Output.format(
            "https://factory.talos.dev/image/{}/{}/metal-amd64.iso",
            self._schematic.id,
            host_config.version,
        )
        self.installer = Output.format(
            "factory.talos.dev/installer-secureboot/{}:{}",
            self._schematic.id,
            host_config.version,
        )

        pulumi.data.export(f"cluster.image.{self._name}.schematic", self.id)
        pulumi.data.export(f"cluster.image.{self._name}.url", self.url)

        self.register_outputs({})
