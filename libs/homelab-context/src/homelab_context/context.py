from typing import Any, Self

from homelab_types import BaseModel
from pydantic import SerializationInfo

from .reference import Reference


class Context(BaseModel):
    references: dict[type[Reference], Any] = {}

    @classmethod
    def from_serialization_info(cls, info: SerializationInfo) -> Self:
        return cls(**(info.context or {}))

    def to_serialization_context(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__class__.model_fields}

    def get[T](self, reference: type[Reference], type: type[T]) -> T:
        data = self.references[reference]
        if not isinstance(data, type):
            raise TypeError(f"Reference data is not an instance of {type}: {data}")
        return data

    def set(self, reference: type[Reference], data: Any) -> None:
        self.references[reference] = data
