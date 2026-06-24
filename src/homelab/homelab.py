from homelab_config import Config


class Homelab:
    def __init__(self) -> None:
        self.config = Config.load()
