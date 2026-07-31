from typing import ClassVar

import pulumi_kubernetes as kubernetes
from homelab_context import Context
from homelab_model import BaseModel, JsonModel
from pulumi import ComponentResource, Output, ResourceOptions

from .. import config as config_
from .. import custom_resource, namespace


class GatewayClass(BaseModel):
    name: Output[str]
    service_prefix: str


class Gateway(BaseModel):
    name: Output[str]
    ip: Output[str]


class Gateways(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "gateway"

    def __init__(
        self,
        context: Context,
        name: str,
        config: config_.network.gateway.Config,
        *,
        opts: ResourceOptions,
        label: config_.label.Config,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config
        self._label = label

        self.build_namespace()
        self.build_classes()
        self.build_gateways()

    def build_namespace(self) -> None:
        self._namespace = namespace.Namespace(self._config.namespace, opts=self._child_opts, label=self._label)

    def build_classes(self) -> None:
        self._classes = {
            name: GatewayClass(
                name=custom_resource.CustomResource(
                    self._context,
                    f"{name}-gateway-class",
                    config_.custom_resource.Config(
                        api_version="gateway.networking.k8s.io/v1",
                        kind="GatewayClass",
                        spec=JsonModel(
                            {
                                "controllerName": "io.cilium/gateway-controller",
                                "parametersRef": {
                                    "group": "cilium.io",
                                    "kind": "CiliumGatewayClassConfig",
                                    "name": custom_resource.CustomResource(
                                        self._context,
                                        f"{name}-gateway-class-config",
                                        config_.custom_resource.Config(
                                            api_version="cilium.io/v2alpha1",
                                            kind="CiliumGatewayClassConfig",
                                            spec=config.spec,
                                        ),
                                        opts=self._child_opts,
                                        namespace=self._namespace,
                                    ).name,
                                    "namespace": self._namespace.name,
                                },
                            }
                        ),
                    ),
                    opts=self._child_opts,
                    namespace=self._namespace,
                ).name,
                service_prefix="cilium-gateway-",
            )
            for name, config in self._config.cilium.classes.items()
        }

    def build_gateways(self) -> None:
        self._gateways: dict[str, Gateway] = {}
        for name, gateway_config in self._config.gateways.items():
            resource_name = f"{name}-gateway"
            gateway_class = self._classes[gateway_config.class_]
            gateway = custom_resource.CustomResource(
                self._context,
                resource_name,
                config_.custom_resource.Config(
                    api_version="gateway.networking.k8s.io/v1",
                    kind="Gateway",
                    spec=JsonModel(
                        {
                            "gatewayClassName": gateway_class.name,
                            "listeners": [
                                {"name": name, "protocol": listener.protocol, "port": listener.port}
                                for name, listener in gateway_config.listeners.items()
                            ],
                            "allowedListeners": {"namespaces": {"from": "All"}},
                        }
                    ),
                ),
                opts=self._child_opts,
                namespace=self._namespace,
            )
            gateway_name = gateway.name

            def ip_or_error(spec: kubernetes.core.v1.outputs.ServiceSpec) -> str:
                if not spec.cluster_ip:
                    raise ValueError(f"Gateway service cluster ip not found: {spec}")
                return spec.cluster_ip

            gateway_ip = kubernetes.core.v1.Service.get(
                resource_name,
                Output.concat(self._namespace.name, "/", gateway_class.service_prefix, gateway_name),
                opts=self._child_opts.merge(ResourceOptions(depends_on=[gateway.resource])),
            ).spec.apply(ip_or_error)

            self._gateways[name] = Gateway(name=gateway_name, ip=gateway_ip)
