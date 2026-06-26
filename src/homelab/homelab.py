import homelab_config as config
from homelab_cluster.cluster import Cluster


class Homelab:
    def __init__(self) -> None:
        self._config = config.Config.load()

        self._cluster = Cluster(self._config.cluster, opts=None)
