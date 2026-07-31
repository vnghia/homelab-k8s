import homelab_pulumi as pulumi
import pulumi_kubernetes as kubernetes
from pulumi import ResourceOptions

from . import common, config


class Namespace:
    def __init__(self, config: config.namespace.Config, *, opts: ResourceOptions, label: config.label.Config) -> None:
        self._name = config.name
        self._config = config
        self._label = label
        self._namespace = kubernetes.core.v1.Namespace(
            self._name, metadata=kubernetes.meta.v1.ObjectMetaArgs(labels=self._config.spec.to_labels()), opts=opts
        )
        self.name = common.metadata.name(self._namespace.metadata)
        pulumi.data.export(f"namespace.{self._name}", self.name)

    def build_labels(self, *, apps: dict[str, str] | None = None) -> dict[str, str]:
        return {f"{self._label.app}/name": self._name} | (
            {f"{self._label.app}/{key}": value for key, value in (apps or {}).items()}
        )
