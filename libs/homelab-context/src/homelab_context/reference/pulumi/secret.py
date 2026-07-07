from typing import Literal

from homelab_types import BaseModel
from pulumi import Output
from pydantic import ConfigDict, SerializationInfo, model_serializer

from .. import common


class Secret(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kind: Literal["pulumi/secret"]
    type: common.type.Type
    path: str

    @model_serializer(mode="plain")
    def serialize(self, info: SerializationInfo) -> Output[common.type.PythonType]:
        from ... import Context

        context = Context.from_serialization_info(info)
        return context.pulumi_secrets.apply(
            lambda secrets: common.data.resolve(secrets, self.type, self.path)
        )
