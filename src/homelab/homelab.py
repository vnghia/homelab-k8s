from homelab_config import Config
from homelab_host.cluster import Cluster


class Homelab:
    def __init__(self) -> None:
        self._config = Config.load()

        self._cluster = Cluster(self._config.cluster, opts=None)
