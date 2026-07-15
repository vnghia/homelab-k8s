import typing

import homelab_context as context
from homelab_model import BaseModel
from pulumi import Output
from pydantic import SerializationInfo, model_serializer

from . import app


class Data(BaseModel):
    apps: dict[str, app.App]


class Reference(context.Reference, kind="kubernetes/app"):
    name: str | None

    @typing.override
    @model_serializer(mode="plain")
    def serialize(
        self, info: SerializationInfo
    ) -> context.reference.type.PythonType | Output[context.reference.type.PythonType]:
        from . import context as context_

        app = context_.Context.from_serialization_info(info)
        return self.resolve(app.get(self.__class__, Data).apps[self.name or app.name])
