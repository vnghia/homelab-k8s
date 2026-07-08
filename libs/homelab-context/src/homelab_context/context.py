from typing import Any, ClassVar, Self

from homelab_types import BaseModel
from pydantic import SerializationInfo

from .reference import Reference


class Context:
    CONTEXT_KEY: ClassVar[str] = "context"

    def __init__(self) -> None:
        self.__data: dict[type[Reference], Any] = {}

    @classmethod
    def from_serialization_info(cls, info: SerializationInfo) -> Self:
        context = (info.context or {})[cls.CONTEXT_KEY]
        if not isinstance(context, cls):
            raise TypeError("Serialization context is not an instance of type Context")
        return context

    def to_serialization_context(self) -> dict[str, Any]:
        return {self.CONTEXT_KEY: self}

    def get[T: BaseModel](self, reference: type[Reference], type: type[T]) -> T:
        data = self.__data[reference]
        if not isinstance(data, type):
            raise TypeError(f"Reference data is not an instance of {type}: {data}")
        return data

    def set(self, reference: type[Reference], data: Any) -> None:
        self.__data[reference] = data
