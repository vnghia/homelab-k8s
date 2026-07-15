import functools
import typing
from typing import Any

import homelab_context as context
import pulumi
from homelab_model import BaseModel
from pulumi import Output
from pydantic import SerializationInfo, model_serializer


class Data(BaseModel):
    _config: pulumi.Config = pulumi.Config()

    @functools.cached_property
    def config(self) -> str:
        return self._config.require("config")

    @functools.cached_property
    def secrets(self) -> Output[Any]:
        return self._config.require_secret_object("secrets")


class Secret(context.Reference, kind="pulumi/secret"):
    @typing.override
    @model_serializer(mode="plain")
    def serialize(
        self, info: SerializationInfo
    ) -> context.reference.type.PythonType | Output[context.reference.type.PythonType]:
        return context.Context.from_serialization_info(info).get(self.__class__, Data).secrets.apply(self.resolve)
