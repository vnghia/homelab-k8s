from typing import Any, Self

import homelab_context as context
from homelab_types import BaseModel as TypesBaseModel
from homelab_types import RootModel as TypesRootModel
from pydantic import (
    ConfigDict,
    ModelWrapValidatorHandler,
    model_validator,
)


class BaseModel(TypesBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class RootModel[T](TypesRootModel[T]):
    pass


class JsonModel(RootModel[dict[str, Any]]):
    @model_validator(mode="wrap")
    @classmethod
    def validate_reference(
        cls, data: Any, handler: ModelWrapValidatorHandler[Self]
    ) -> Self:
        return handler(
            {
                key: context.reference.recursive_validate(value)
                for key, value in data.items()
            }
        )
