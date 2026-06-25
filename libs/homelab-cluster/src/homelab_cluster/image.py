from typing import ClassVar

import pulumi
import pulumiverse_talos as talos
from homelab_pulumi import OutputSerializer
from pulumi import ComponentResource, Output, ResourceOptions

from .config import ClusterConfig, ImageConfig


class Image(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "image"

    def __init__(
        self,
        name: str,
        config: ImageConfig,
        *,
        opts: ResourceOptions | None,
        cluster_config: ClusterConfig,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config

        self._extensions = talos.imagefactory.get_extensions_versions_output(
            talos_version=cluster_config.version.talos,
            filters=talos.imagefactory.GetExtensionsVersionsFiltersArgs(
                names=self._config.extensions
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

        self.id = self._schematic.id
        self.url = Output.format(
            "https://factory.talos.dev/image/{}/{}/metal-amd64.iso",
            self._schematic.id,
            cluster_config.version.talos,
        )
        self.installer = Output.format(
            "factory.talos.dev/installer-secureboot/{}:{}",
            self._schematic.id,
            cluster_config.version.talos,
        )

        pulumi.export(f"cluster.image.{self._name}.schematic", self.id)
        pulumi.export(f"cluster.image.{self._name}.url", self.url)

        self.register_outputs({})
