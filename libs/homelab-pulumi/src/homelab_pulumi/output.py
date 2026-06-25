from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import orjson
import yaml_rs
from pulumi import Output
from pydantic import GetPydanticSchema

type PydanticOutput[T] = Annotated[
    Output[T], GetPydanticSchema(lambda _s, handler: handler(Any))
]


class OutputSerializer:
    DEFAULT_LOADER: ClassVar[Callable[[str], Any]] = orjson.loads
    DEFAULT_DUMPER: ClassVar[Callable[[Any], str]] = lambda data: orjson.dumps(
        data
    ).decode()

    @classmethod
    def serialize(
        cls,
        data: Any,
        loader: Callable[[str], Any] | None = None,
        dumper: Callable[[Any], str] | None = None,
    ) -> Output[str]:
        loader_ = loader or cls.DEFAULT_LOADER
        dumper_ = dumper or cls.DEFAULT_DUMPER
        return Output.json_dumps(data).apply(lambda data: dumper_(loader_(data)))

    @classmethod
    def yaml(cls, data: Any) -> Output[str]:
        return cls.serialize(data, dumper=yaml_rs.dumps)
