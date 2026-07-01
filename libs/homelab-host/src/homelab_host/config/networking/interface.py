from homelab_model import BaseModel


class Config(BaseModel):
    dhcpv4: bool
    dhcpv6: bool
