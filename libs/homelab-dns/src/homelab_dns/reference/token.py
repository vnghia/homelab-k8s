import homelab_context as context
from homelab_context import Context
from pulumi import Output
from pydantic import SerializationInfo, model_serializer


class Reference(context.Reference, kind="dns/token"):
    @model_serializer(mode="plain")
    def serialize(
        self, info: SerializationInfo
    ) -> context.reference.type.PythonType | Output[context.reference.type.PythonType]:
        from .. import token

        return self.resolve(
            Context.from_serialization_info(info).get(self.__class__, token.Token)
        )
