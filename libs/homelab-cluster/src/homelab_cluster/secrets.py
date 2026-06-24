import pulumiverse_talos as talos
from pulumi import ResourceOptions


class ClusterSecrets:
    def __init__(self, *, opts: ResourceOptions | None, version: str) -> None:
        self._secret = talos.machine.Secrets(
            "secrets", opts=opts, talos_version=version
        )
