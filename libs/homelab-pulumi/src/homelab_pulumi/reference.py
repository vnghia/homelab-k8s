import functools
from typing import Any

import homelab_context as context
import pulumi
from homelab_context import Context, Reference
from homelab_model import BaseModel
from pulumi import Output
from pydantic import ConfigDict, SerializationInfo, model_serializer


class Data(BaseModel):
    _config: pulumi.Config = pulumi.Config()

    @functools.cached_property
    def config(self) -> str:
        return self._config.require("config")

    @functools.cached_property
    def secrets(self) -> Output[Any]:
        return self._config.require_secret_object("secrets")


class Secret(Reference, kind="pulumi/secret"):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_serializer(mode="plain")
    def serialize(
        self, info: SerializationInfo
    ) -> Output[context.reference.type.PythonType]:
        context = Context.from_serialization_info(info)
        return context.get(self.__class__, Data).secrets.apply(self.resolve)
