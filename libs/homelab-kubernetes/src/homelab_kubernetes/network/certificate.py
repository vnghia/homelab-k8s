from homelab_context import Context
from pulumi import ResourceOptions

from .. import app, config


class Certificate(app.App[config.network.certificate.Config]):
    def __init__(
        self,
        context: Context,
        config: config.network.certificate.Config,
        *,
        opts: ResourceOptions,
        label: config.label.Config,
        data: app.reference.Data,
    ) -> None:
        super().__init__(
            context, config.namespace.name, config, opts=opts, label=label, data=data, register_output=False
        )
