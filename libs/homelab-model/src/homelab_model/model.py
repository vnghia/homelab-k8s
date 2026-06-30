from typing import Any

from homelab_context import Context
from homelab_types import BaseModel as TypesBaseModel
from homelab_types import RootModel as TypesRootModel
from pydantic import (
    ConfigDict,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    model_serializer,
)


class BaseModel(TypesBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class RootModel[T](TypesRootModel[T]):
    pass


class JsonModel(RootModel[dict[str, Any]]):
    @model_serializer(mode="wrap")
    def serialize_model(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
        context = (info.context or {})["context"]
        if not isinstance(context, Context):
            raise TypeError("Serialization context is not an instance of type Context")
        return context.resolve(handler(self))
