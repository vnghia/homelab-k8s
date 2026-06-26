from typing import ClassVar

import homelab_common as common
import homelab_pulumi as pulumi
import pulumi_tailscale as tailscale
import pulumiverse_talos as talos
from pulumi import ComponentResource, Input, Output, ResourceOptions

from homelab_cluster.image import Image
from homelab_cluster.secrets import Secrets

from . import config


class Host(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "host"

    def __init__(
        self,
        name: str,
        config: config.host.Config,
        *,
        opts: ResourceOptions | None,
        cluster_config: config.Config,
        cluster_secrets: Secrets,
        cluster_images: dict[str, Image],
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._config = config
        self._cluster_config = cluster_config
        self._cluster_images = cluster_images

        self._hostname = common.string.add_prefix(
            pulumi.constant.STACK,
            common.string.add_prefix(
                self._cluster_config.domain.prefix, self._name, separator="-"
            ),
            separator="-",
        )
        self._endpoint = common.string.add_suffix(
            self._hostname,
            self._cluster_config.domain.name,
            separator=".",
        )

        self._client_configuration = cluster_secrets.client_configuration
        self._machine_secrets = cluster_secrets.machine_secrets
        self._machine_bootstrap = None

        self._machine_configurations: list[Output[str]] = [
            self.get_machine_configuration()
        ]

        self.apply_initial_patches()
        self.apply_multihoming_patches()

        if self._config.stage == config.stage.INITIAL:
            self.register_outputs({})
            return

        self._machine_bootstrap = (
            talos.machine.Bootstrap(
                self._name,
                opts=self._child_opts,
                client_configuration=cluster_secrets.client_configuration.to_args(),
                node=self._endpoint,
            )
            if self._cluster_config.bootstrap == self._name
            else None
        )

        self.apply_features_patches()
        self.apply_tailscale_patches()

        self.register_outputs({})

    def get_machine_configuration(self) -> Output[str]:
        return talos.machine.get_configuration_output(
            cluster_endpoint=self._cluster_config.endpoint,
            cluster_name=self._cluster_config.name,
            machine_type="controlplane" if self._config.features.worker else "worker",
            machine_secrets=self._machine_secrets.to_args(),
            talos_version=self._cluster_config.version.talos,
            kubernetes_version=self._cluster_config.version.k8s,
        ).apply(
            lambda machine_configuration: machine_configuration.machine_configuration
        )

    def apply_patches(self, name: str, patches: list[Input[str]]) -> None:
        self._machine_configurations.append(
            talos.machine.ConfigurationApply(
                name,
                opts=self._child_opts.merge(
                    ResourceOptions(depends_on=self._machine_bootstrap)
                ),
                node=self._endpoint,
                client_configuration=self._client_configuration.to_args(),
                machine_configuration_input=self._machine_configurations[-1],
                config_patches=patches,
            ).machine_configuration
        )

    def apply_initial_patches(self) -> None:
        self.apply_patches(
            "initial",
            [
                pulumi.data.serialize.yaml(
                    {
                        "machine": {
                            "install": {
                                "disk": self._config.install.disk,
                                "image": self._cluster_images[
                                    self._config.install.image
                                ].installer,
                            }
                        }
                    },
                    False,
                ),
                pulumi.data.serialize.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "HostnameConfig",
                        "hostname": self._endpoint,
                        "auto": "off",
                    },
                    True,
                ),
                pulumi.data.serialize.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "VolumeConfig",
                        "name": "STATE",
                        "encryption": {
                            "provider": "luks2",
                            "keys": [{"nodeID": {}, "slot": 0}],
                        },
                    },
                    True,
                ),
                pulumi.data.serialize.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "VolumeConfig",
                        "name": "EPHEMERAL",
                        "encryption": {
                            "provider": "luks2",
                            "keys": [{"nodeID": {}, "slot": 0, "lockToState": True}],
                        },
                        "provisioning": {
                            "diskSelector": {
                                "match": self._config.install.volumes.ephemeral.selector,
                            },
                            "minSize": self._config.install.volumes.ephemeral.min_size,
                            "maxSize": self._config.install.volumes.ephemeral.max_size,
                            "grow": True,
                        },
                    },
                    True,
                ),
            ],
        )

    def apply_multihoming_patches(self) -> None:
        valid_subnets = ["192.168.0.0/16", "100.64.0.0/10"]
        self.apply_patches(
            "networking-multihoming",
            [
                pulumi.data.serialize.yaml(
                    {
                        "machine": {
                            "kubelet": {"nodeIP": {"validSubnets": valid_subnets}}
                        }
                    },
                    True,
                ),
                pulumi.data.serialize.yaml(
                    {"cluster": {"etcd": {"advertisedSubnets": valid_subnets}}}, True
                ),
            ],
        )

    def apply_features_patches(self) -> None:
        if self._config.features.controlplane and self._config.features.worker:
            self.apply_patches(
                "worker",
                [
                    pulumi.data.serialize.yaml(
                        {"cluster": {"allowSchedulingOnControlPlanes": True}}, True
                    )
                ],
            )
            if self._config.features.loadbalancer:
                self.apply_patches(
                    "loadbalancer",
                    [
                        pulumi.data.serialize.yaml(
                            {
                                "machine": {
                                    "nodeLabels": {
                                        "node.kubernetes.io/exclude-from-external-load-balancers": {
                                            "$patch": "delete"
                                        }
                                    }
                                }
                            },
                            True,
                        )
                    ],
                )

    def apply_tailscale_patches(self) -> None:
        self.apply_patches(
            "tailscale",
            [
                pulumi.data.serialize.yaml(
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "ExtensionServiceConfig",
                        "name": "tailscale",
                        "environment": [
                            Output.concat(
                                "TS_AUTHKEY=",
                                tailscale.TailnetKey(
                                    self._name,
                                    opts=self._child_opts,
                                    ephemeral=False,
                                    expiry=5 * 60,
                                    preauthorized=True,
                                    reusable=False,
                                ).key,
                            ),
                            "TS_AUTH_ONCE=true",
                            "TS_TAILSCALED_EXTRA_ARGS=--no-logs-no-support",
                            "TS_ACCEPT_DNS=false",
                            f"TS_HOSTNAME={self._hostname}",
                        ],
                    },
                    False,
                )
            ],
        )
