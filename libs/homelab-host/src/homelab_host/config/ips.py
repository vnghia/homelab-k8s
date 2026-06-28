from ipaddress import IPv4Address

from homelab_model import BaseModel


class Config(BaseModel):
    tailscale: IPv4Address
