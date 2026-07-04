from typing import ClassVar

import pulumi_kubernetes as kubernetes
from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import common, config, namespace


class Gateway(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "gateway"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config.networking.gateway.Config,
        *,
        opts: ResourceOptions,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self.build_namespace()
        self.build_classes()
        self.build_gateways()

    def build_namespace(self) -> None:
        self._namespace = namespace.Namespace(
            self._config.namespace, opts=self._child_opts
        )

    def build_classes(self) -> None:
        self._classes = {
            name: common.metadata.name(
                kubernetes.apiextensions.CustomResource(
                    f"{name}-gateway-class",
                    opts=self._child_opts,
                    api_version="gateway.networking.k8s.io/v1",
                    kind="GatewayClass",
                    metadata=kubernetes.meta.v1.ObjectMetaArgs(
                        namespace=self._namespace.name
                    ),
                    spec={
                        "controllerName": "io.cilium/gateway-controller",
                        "parametersRef": {
                            "group": "cilium.io",
                            "kind": "CiliumGatewayClassConfig",
                            "name": common.metadata.name(
                                kubernetes.apiextensions.CustomResource(
                                    f"{name}-gateway-class-config",
                                    opts=self._child_opts,
                                    api_version="cilium.io/v2alpha1",
                                    kind="CiliumGatewayClassConfig",
                                    metadata=kubernetes.meta.v1.ObjectMetaArgs(
                                        namespace=self._namespace.name
                                    ),
                                    spec=config.spec.model_dump(
                                        context={"context": self._context}
                                    ),
                                ).__dict__["metadata"]
                            ),
                            "namespace": self._namespace.name,
                        },
                    },
                ).__dict__["metadata"]
            )
            for name, config in self._config.cilium.classes.items()
        }

    def build_gateways(self) -> None:
        self._gateways = {
            name: common.metadata.name(
                kubernetes.apiextensions.CustomResource(
                    f"{name}-gateway",
                    opts=self._child_opts,
                    api_version="gateway.networking.k8s.io/v1",
                    kind="Gateway",
                    metadata=kubernetes.meta.v1.ObjectMetaArgs(
                        namespace=self._namespace.name
                    ),
                    spec={
                        "gatewayClassName": self._classes[config.class_],
                        "listeners": [
                            {
                                "name": name,
                                "protocol": listener.protocol,
                                "port": listener.port,
                            }
                            for name, listener in config.listeners.items()
                        ],
                        "allowedListeners": {"namespaces": {"from": "All"}},
                    },
                ).__dict__["metadata"]
            )
            for name, config in self._config.gateways.items()
        }
