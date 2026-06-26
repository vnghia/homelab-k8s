from typing import Annotated, Any

import pulumi
from pydantic import GetPydanticSchema

type Output[T] = Annotated[
    pulumi.Output[T], GetPydanticSchema(lambda _s, handler: handler(Any))
]

type Input[T] = T | Output[T]
