from typing import ClassVar

import homelab_common as common
import homelab_kubernetes as kubernetes
import homelab_pulumi as pulumi
import pulumi_tailscale as tailscale
import pulumiverse_talos as talos
from homelab_context import Context
from pulumi import ComponentResource, Input, Output, ResourceOptions

from . import config
from .image import Image
from .secrets import Secrets


class Machine(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "machine"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.machine.Config,
        *,
        opts: ResourceOptions | None,
        host_config: config.Config,
        host_secrets: Secrets,
        host_images: dict[str, Image],
        kubernetes_config: kubernetes.config.Config,
        cluster_name: str,
        cluster_endpoint: str,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._host_config = host_config
        self._host_images = host_images
        self._kubernetes_config = kubernetes_config
        self._cluster_name = cluster_name
        self._cluster_endpoint = cluster_endpoint

        self._hostname = common.string.add_prefix(
            pulumi.constant.STACK,
            common.string.add_prefix(
                self._kubernetes_config.domain.prefix, self._name, separator="-"
            ),
            separator="-",
        )
        self._endpoint = common.string.add_suffix(
            self._hostname,
            self._kubernetes_config.domain.name,
            separator=".",
        )

        self._client_configuration = host_secrets.client_configuration
        self._machine_secrets = host_secrets.machine_secrets
        self._machine_bootstrap = None

        self._machine_configuration = self.get_machine_configuration()
        self._applied_configurations: list[talos.machine.ConfigurationApply] = []

        self.apply_initial_patches()
        self.apply_networking_initial_patches()
        self.apply_networking_gateway_api_patches()
        self.apply_networking_cilium_patches()

        self._machine_bootstrap = (
            talos.machine.Bootstrap(
                self._name,
                opts=self._child_opts.merge(
                    ResourceOptions(depends_on=self._applied_configurations[-1])
                ),
                client_configuration=self._client_configuration.to_args(),
                node=self._endpoint,
            )
            if self._host_config.bootstrap == self._name
            else None
        )

        if self._config.stage == config.stage.INITIAL:
            self.register_outputs({})
            return

        self.apply_features_patches()
        self.apply_tailscale_patches()

        self.register_outputs({})

    def get_machine_configuration(self) -> Output[str]:
        return talos.machine.get_configuration_output(
            cluster_name=self._cluster_name,
            cluster_endpoint=self._cluster_endpoint,
            machine_type="controlplane" if self._config.features.worker else "worker",
            machine_secrets=self._machine_secrets.to_args(),
            talos_version=self._host_config.version,
            kubernetes_version=self._kubernetes_config.version,
        ).apply(
            lambda machine_configuration: machine_configuration.machine_configuration
        )

    def apply_patches(self, name: str, patches: list[Input[str]]) -> None:
        machine_configuration = (
            self._applied_configurations[-1].machine_configuration
            if self._applied_configurations
            else self._machine_configuration
        )
        self._applied_configurations.append(
            talos.machine.ConfigurationApply(
                name,
                opts=self._child_opts.merge(
                    ResourceOptions(depends_on=self._machine_bootstrap)
                ),
                node=self._endpoint,
                client_configuration=self._client_configuration.to_args(),
                machine_configuration_input=machine_configuration,
                config_patches=patches,
            )
        )

    def apply_initial_patches(self) -> None:
        self.apply_patches(
            "initial",
            [
                pulumi.data.serialize.yaml(
                    self._context,
                    {
                        "machine": {
                            "install": {
                                "disk": self._config.install.disk,
                                "image": self._host_images[
                                    self._config.install.image
                                ].installer,
                            }
                        }
                    },
                    direct=False,
                ),
                pulumi.data.serialize.yaml(
                    self._context,
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "HostnameConfig",
                        "hostname": self._endpoint,
                        "auto": "off",
                    },
                    direct=True,
                ),
                pulumi.data.serialize.yaml(
                    self._context,
                    {
                        "apiVersion": "v1alpha1",
                        "kind": "VolumeConfig",
                        "name": "STATE",
                        "encryption": {
                            "provider": "luks2",
                            "keys": [{"nodeID": {}, "slot": 0}],
                        },
                    },
                    direct=True,
                ),
                pulumi.data.serialize.yaml(
                    self._context,
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
                    direct=True,
                ),
            ],
        )

    def apply_networking_initial_patches(self) -> None:
        valid_subnets = ["192.168.0.0/16", "100.64.0.0/10"]
        self.apply_patches(
            "networking-initial",
            [
                pulumi.data.serialize.yaml(
                    self._context,
                    {
                        "machine": {
                            "kubelet": {"nodeIP": {"validSubnets": valid_subnets}}
                        }
                    },
                    direct=True,
                ),
                pulumi.data.serialize.yaml(
                    self._context,
                    {"cluster": {"etcd": {"advertisedSubnets": valid_subnets}}},
                    direct=True,
                ),
            ],
        )

    def apply_networking_gateway_api_patches(self) -> None:
        if self._config.features.controlplane:
            gateway_config = self._kubernetes_config.networking.gateway
            self.apply_patches(
                "networking-gateway-api",
                [
                    pulumi.data.serialize.yaml(
                        self._context,
                        {
                            "cluster": {
                                "extraManifests": [
                                    f"https://github.com/kubernetes-sigs/gateway-api/releases/download/{gateway_config.version}/{gateway_config.type}-install.yaml"
                                ]
                            }
                        },
                        direct=True,
                    ),
                ],
            )

    def apply_networking_cilium_patches(self) -> None:
        if self._config.features.controlplane:
            cilium_config = self._kubernetes_config.networking.cilium
            self.apply_patches(
                "networking-cilium",
                [
                    pulumi.data.serialize.yaml(
                        self._context,
                        {
                            "cluster": {
                                "network": {"cni": {"name": "none"}},
                                "proxy": {"disabled": True},
                            }
                        },
                        direct=True,
                    ),
                    pulumi.data.serialize.yaml(
                        self._context,
                        {
                            "machine": {
                                "features": {
                                    "hostDNS": {
                                        # See this discussion for more context: https://github.com/siderolabs/talos/pull/9200
                                        "forwardKubeDNSToHost": False
                                    }
                                },
                            }
                        },
                        direct=True,
                    ),
                    pulumi.data.serialize.yaml(
                        self._context,
                        {
                            "cluster": {
                                "inlineManifests": [
                                    {
                                        "name": "cilium",
                                        "contents": pulumi.data.serialize.yaml(
                                            self._context,
                                            [
                                                {
                                                    "apiVersion": "v1",
                                                    "kind": "Namespace",
                                                    "metadata": {
                                                        "labels": {
                                                            "pod-security.kubernetes.io/enforce": "privileged",
                                                            "pod-security.kubernetes.io/audit": "privileged",
                                                            "pod-security.kubernetes.io/warn": "privileged",
                                                        },
                                                        "name": cilium_config.namespace,
                                                    },
                                                }
                                            ]
                                            + [
                                                manifest.model_dump(
                                                    context={"context": self._context}
                                                )
                                                for manifest in cilium_config.manifests
                                            ],
                                            direct=False,
                                        ),
                                    }
                                ]
                            }
                        },
                        direct=False,
                    ),
                ],
            )

    def apply_features_patches(self) -> None:
        if self._config.features.controlplane and self._config.features.worker:
            self.apply_patches(
                "worker",
                [
                    pulumi.data.serialize.yaml(
                        self._context,
                        {"cluster": {"allowSchedulingOnControlPlanes": True}},
                        direct=True,
                    )
                ],
            )
            if self._config.features.loadbalancer:
                self.apply_patches(
                    "loadbalancer",
                    [
                        pulumi.data.serialize.yaml(
                            self._context,
                            {
                                "machine": {
                                    "nodeLabels": {
                                        "node.kubernetes.io/exclude-from-external-load-balancers": {
                                            "$patch": "delete"
                                        }
                                    }
                                }
                            },
                            direct=True,
                        )
                    ],
                )

    def apply_tailscale_patches(self) -> None:
        self.apply_patches(
            "tailscale",
            [
                pulumi.data.serialize.yaml(
                    self._context,
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
                    direct=False,
                )
            ],
        )
