import homelab_cluster as cluster
import homelab_config as config
import homelab_context as context


class Homelab:
    def __init__(self) -> None:
        self._context = context.Context()
        self._config = config.Config.load(self._context)
        self._cluster = cluster.Cluster(self._context, self._config.cluster, opts=None)
