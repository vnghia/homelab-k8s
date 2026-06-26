from ipaddress import IPv4Address

from homelab_types import BaseModel


class Config(BaseModel):
    tailscale: IPv4Address
