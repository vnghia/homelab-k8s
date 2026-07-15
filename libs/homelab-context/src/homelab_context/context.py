from typing import Any, Self

from pydantic import SerializationInfo, dataclasses

from .reference import Reference


@dataclasses.dataclass
class Context:
    references: dict[type[Reference], Any]

    @classmethod
    def from_serialization_info(cls, info: SerializationInfo) -> Self:
        return cls(**(info.context or {}))

    def asdict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__dataclass_fields__}

    def get[T](self, reference: type[Reference], type: type[T]) -> T:
        data = self.references[reference]
        if not isinstance(data, type):
            raise TypeError(f"Reference data is not an instance of {type}: {data}")
        return data

    def set(self, reference: type[Reference], data: Any) -> None:
        self.references[reference] = data
