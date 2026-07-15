import homelab_cluster as cluster
import homelab_config as config
import homelab_context as context
import homelab_dns as dns
import homelab_pulumi as pulumi


class Homelab:
    def __init__(self) -> None:
        self._pulumi_data = pulumi.reference.Data()

        self._context = context.Context()
        self._context.set(pulumi.reference.Secret, pulumi.reference.Data())
        self._config = config.Config.load(self._pulumi_data)

        self._dns = dns.Dns(
            self._config.cluster.name,
            self._context,
            self._config.dns,
            opts=None,
        )
        self._cluster = cluster.Cluster(self._context, self._config.cluster, opts=None)
