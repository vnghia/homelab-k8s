import functools
import typing
from typing import Any

import homelab_context as context
import pulumi
from homelab_context import Context, Reference
from homelab_model import BaseModel
from pulumi import Output


class Data(BaseModel):
    _config: pulumi.Config = pulumi.Config()

    @functools.cached_property
    def config(self) -> str:
        return self._config.require("config")

    @functools.cached_property
    def secrets(self) -> Output[Any]:
        return self._config.require_secret_object("secrets")


class Secret(Reference, kind="pulumi/secret"):
    @typing.override
    def resolve(
        self,
        context: Context,
    ) -> Output[context.reference.type.PythonType]:
        return context.get(self.__class__, Data).secrets.apply(self.resolve_data)
