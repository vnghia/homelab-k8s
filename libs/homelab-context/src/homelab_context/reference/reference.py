import abc
import typing
from typing import Any, ClassVar

from homelab_types import BaseModel
from pulumi import Output
from pydantic import ConfigDict, SerializationInfo, field_validator, model_serializer

from .data import resolve
from .type import PythonType, Type

if typing.TYPE_CHECKING:
    from ..context import Context


class Reference(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    KINDS: ClassVar[dict[str, type[Reference]]] = {}

    KIND: ClassVar[str]

    kind: str = ""
    type: Type
    path: str

    @classmethod
    def __init_subclass__(cls, kind: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    @typing.override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        kind = kwargs.pop("kind")
        if not isinstance(kind, str):
            raise TypeError("Reference kind has to be a string")

        cls.KINDS[kind] = cls
        cls.KIND = kind

    @field_validator("kind", mode="plain")
    @classmethod
    def set_kind(cls, _: Any) -> str:
        return cls.KIND

    @classmethod
    def recursive_validate(cls, data: Any) -> Any:
        if isinstance(data, list):
            return [cls.recursive_validate(item) for item in data]
        if isinstance(data, dict):
            if (kind := data.get("kind")) and (kind in cls.KINDS):
                return cls.KINDS[kind].model_validate(data)
            return {key: cls.recursive_validate(value) for key, value in data.items()}
        return data

    def resolve_data(self, data: Any) -> PythonType | Output[PythonType]:
        return resolve(data, self.type, self.path)

    @abc.abstractmethod
    def resolve(self, context: Context) -> PythonType | Output[PythonType]: ...

    @model_serializer(mode="plain")
    def serialize(
        self,
        info: SerializationInfo,
    ) -> PythonType | Output[PythonType]:
        from ..context import Context

        return self.resolve(Context.from_serialization_info(info))
