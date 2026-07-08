import homelab_context as context
from homelab_context import Context, Reference
from homelab_model import BaseModel
from pulumi import Output
from pydantic import SerializationInfo, model_serializer

from . import token


class Data(BaseModel):
    token: token.Token


class Token(Reference, kind="dns/token"):
    @model_serializer(mode="plain")
    def serialize(
        self, info: SerializationInfo
    ) -> Output[context.reference.type.PythonType]:
        return Output.from_input(
            Context.from_serialization_info(info).get(self.__class__, Data).token.data
        ).apply(self.resolve)
