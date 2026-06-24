from homelab_config import Config
from homelab_host import Host


class Homelab:
    def __init__(self) -> None:
        self._config = Config.load()

        self._hosts = {
            name: Host(name, config, opts=None)
            for name, config in self._config.hosts.root.items()
        }
