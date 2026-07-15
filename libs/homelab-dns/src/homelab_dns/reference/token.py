import typing

import homelab_context as context
from homelab_context import Context
from pulumi import Output


class Reference(context.Reference, kind="dns/token"):
    @typing.override
    def resolve(
        self, context: Context
    ) -> context.reference.type.PythonType | Output[context.reference.type.PythonType]:
        from .. import token

        return self.resolve_data(context.get(self.__class__, token.Token))
