import subprocess
import typing
from pathlib import Path
from typing import Any, ClassVar

import homelab_common as common
import yaml_rs
from homelab_context import Context
from homelab_model import BaseModel, JsonModel
from pulumi import Output, ResourceOptions
from pulumi.dynamic import CreateResult, Resource, ResourceProvider, UpdateResult
from pydantic import ConfigDict


class KustomizeProviderNamespaceProps(BaseModel):
    name: str | Output[str]
    labels: dict[str, str | Output[str]] = {}


class KustomizeProviderProps(BaseModel):
    model_config = ConfigDict(extra="ignore")

    KUSTOMIZE: ClassVar[Path] = common.path.which("kustomize")
    BASE: ClassVar[Path] = common.constant.path.ROOT / ".kubernetes" / "kustomize"

    id: str
    namespace: KustomizeProviderNamespaceProps | None = None
    kustomization: Any

    def build(self) -> str:
        directory = self.BASE / self.id
        directory.mkdir(parents=True, exist_ok=True)
        yaml_rs.dump(self.kustomization, file=directory / "kustomization.yaml")

        manifests = subprocess.check_output(
            [self.KUSTOMIZE, "build", "--enable-helm", directory],
        ).decode()
        if self.namespace:
            manifests += yaml_rs.dumps(
                {
                    "apiVersion": "v1",
                    "kind": "Namespace",
                    "metadata": self.namespace.model_dump(),
                },
            )
        return manifests


class KustomizeProvider(ResourceProvider):
    serialize_as_secret_always = False

    @typing.override
    def create(self, props: dict[str, Any]) -> CreateResult:
        kustomize_props = KustomizeProviderProps(**props)
        return CreateResult(
            id_=kustomize_props.id,
            outs=kustomize_props.model_dump() | {"manifests": kustomize_props.build()},
        )

    @typing.override
    def update(
        self,
        _id: str,
        _olds: dict[str, Any],
        _news: dict[str, Any],
    ) -> UpdateResult:
        kustomize_props = KustomizeProviderProps(**_news)
        return UpdateResult(
            outs=kustomize_props.model_dump() | {"manifests": kustomize_props.build()},
        )


class Kustomize(Resource, module="kubernetes", name="Kustomize"):
    manifests: Output[str]

    def __init__(
        self,
        context: Context,
        opts: ResourceOptions,
        *,
        id: str,
        namespace: KustomizeProviderNamespaceProps | None,
        kustomization: JsonModel,
    ) -> None:
        super().__init__(
            KustomizeProvider(),
            id,
            {
                "id": id,
                "namespace": namespace.model_dump() if namespace else None,
                "kustomization": kustomization.model_dump(
                    context=context.to_serialization_context(),
                ),
                "manifests": None,
            },
            opts.merge(ResourceOptions(additional_secret_outputs=["manifests"])),
        )
