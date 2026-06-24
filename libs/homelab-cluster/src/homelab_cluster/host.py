from typing import ClassVar

import pulumi
import pulumiverse_talos as talos
from homelab_pulumi.data import OutputSerializer
from pulumi import ComponentResource, Output, ResourceOptions

from homelab_cluster.secrets import ClusterSecrets

from .config import HostConfig


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        name: str,
        config: HostConfig,
        *,
        opts: ResourceOptions | None,
        cluser_name: str,
        cluser_version: str,
        cluser_endpoint: str,
        cluser_secrets: ClusterSecrets,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._name = name
        self._config = config

        self._extensions = talos.imagefactory.get_extensions_versions_output(
            talos_version=cluser_version,
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
        pulumi.export(
            f"host.{self._name}.image.url",
            Output.format(
                "https://factory.talos.dev/image/{}/{}/metal-amd64.iso",
                self._schematic.id,
                cluser_version,
            ),
        )

        self.register_outputs({})
