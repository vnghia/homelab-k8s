from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from pydantic import RootModel as PydanticRootModel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        populate_by_name=True,
        revalidate_instances="always",
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
        validation_error_cause=True,
    )


class RootModel[T](PydanticRootModel[T]):
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        revalidate_instances="always",
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
        validation_error_cause=True,
    )
