from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


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
