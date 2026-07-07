from typing import Any, ClassVar, Self

import pulumi
from pydantic import SerializationInfo


class Context:
    CONTEXT_KEY: ClassVar[str] = "context"

    def __init__(self) -> None:
        self.pulumi = pulumi.Config()
        self.pulumi_secrets = self.pulumi.require_secret_object("secrets")

    @classmethod
    def from_serialization_info(cls, info: SerializationInfo) -> Self:
        context = (info.context or {})[cls.CONTEXT_KEY]
        if not isinstance(context, cls):
            raise TypeError("Serialization context is not an instance of type Context")
        return context

    def to_serialization_context(self) -> dict[str, Any]:
        return {self.CONTEXT_KEY: self}
