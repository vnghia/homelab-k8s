from typing import ClassVar

import pulumiverse_talos as talos
from homelab_pulumi.data import OutputSerializer
from pulumi import ComponentResource, Input, Output, ResourceOptions

from homelab_cluster.image import Image
from homelab_cluster.secrets import Secrets

from .config import ClusterConfig, HostConfig, HostStageConfig


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        name: str,
        config: HostConfig,
        *,
        opts: ResourceOptions | None,
        cluster_config: ClusterConfig,
        cluster_secrets: Secrets,
        cluster_images: dict[str, Image],
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config

        self._client_configuration = cluster_secrets.client_configuration
        self._machine_secrets = cluster_secrets.machine_secrets

        self._machine_configurations: list[Output[str]] = [
            talos.machine.get_configuration_output(
                cluster_endpoint=cluster_config.endpoint,
                cluster_name=cluster_config.name,
                machine_type="controlplane"
                if self._config.features.worker
                else "worker",
                machine_secrets=self._machine_secrets.to_args(),
                talos_version=cluster_config.version.talos,
                kubernetes_version=cluster_config.version.k8s,
            ).apply(
                lambda machine_configuration: (
                    machine_configuration.machine_configuration
                )
            )
        ]

        self.apply_patches(
            "initial",
            [
                OutputSerializer.yaml(
                    {
                        "machine": {
                            "install": {
                                "disk": self._config.install.disk,
                                "image": cluster_images[
                                    self._config.install.image
                                ].installer,
                            }
                        }
                    }
                ),
                OutputSerializer.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "HostnameConfig",
                        "hostname": self._config.endpoint,
                        "auto": "off",
                    }
                ),
                OutputSerializer.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "VolumeConfig",
                        "name": "STATE",
                        "encryption": {
                            "provider": "luks2",
                            "keys": [{"nodeID": {}, "slot": 0}],
                        },
                    }
                ),
                OutputSerializer.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "VolumeConfig",
                        "name": "EPHEMERAL",
                        "encryption": {
                            "provider": "luks2",
                            "keys": [{"nodeID": {}, "slot": 0, "lockToState": True}],
                        },
                    }
                ),
            ],
        )

        if self._config.stage == HostStageConfig.INITIAL:
            self.register_outputs({})
            return

        if self._config.features.controlplane and self._config.features.worker:
            self.apply_patches(
                "worker",
                [
                    OutputSerializer.yaml(
                        {"cluster": {"allowSchedulingOnControlPlanes": True}}
                    )
                ],
            )
            if self._config.features.loadbalancer:
                self.apply_patches(
                    "loadbalancer",
                    [
                        OutputSerializer.yaml(
                            {
                                "machine": {
                                    "nodeLabels": {
                                        "node.kubernetes.io/exclude-from-external-load-balancers": {
                                            "$patch": "delete"
                                        }
                                    }
                                }
                            }
                        )
                    ],
                )

        self.register_outputs({})

    def apply_patches(self, name: str, patches: list[Input[str]]) -> None:
        self._machine_configurations.append(
            talos.machine.ConfigurationApply(
                name,
                opts=self._child_opts,
                node=self._config.endpoint,
                client_configuration=self._client_configuration.to_args(),
                machine_configuration_input=self._machine_configurations[-1],
                config_patches=patches,
            ).machine_configuration
        )
