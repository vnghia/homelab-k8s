from typing import ClassVar

from homelab_context import Context
from pulumi import ComponentResource, ResourceOptions

from . import config, reference, token


class Dns(ComponentResource):
    RESOURCE_TYPE: ClassVar[str] = "dns"

    def __init__(
        self,
        name: str,
        context: Context,
        config: config.Config,
        *,
        opts: ResourceOptions | None,
    ) -> None:
        super().__init__(self.RESOURCE_TYPE, name, None, opts)
        self._child_opts = ResourceOptions(parent=self)

        self._context = context
        self._config = config

        self.build_token()
        self.build_data()

    def build_token(self) -> None:
        self._token = token.Token(
            self._name, self._context, self._config, opts=self._child_opts
        )

    def build_data(self) -> None:
        self._data = reference.Data(token=self._token)
        self._context.set(reference.Token, self._data)
