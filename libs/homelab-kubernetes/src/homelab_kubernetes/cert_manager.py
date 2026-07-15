from homelab_context import Context
from pulumi import ResourceOptions

from . import app, config


class CertManager(app.App[config.cert_manager.Config]):
    def __init__(
        self, context: Context, config: config.cert_manager.Config, *, opts: ResourceOptions, data: app.reference.Data
    ) -> None:
        super().__init__(context, config.namespace.name, config, opts=opts, data=data, register_output=False)
