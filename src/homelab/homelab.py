from homelab_cluster.cluster import Cluster
from homelab_config import Config


class Homelab:
    def __init__(self) -> None:
        self._config = Config.load()

        self._cluster = Cluster(self._config.cluster, opts=None)
