from homelab_model import BaseModel


class ProvisioningVolume(BaseModel):
    selector: str
    min_size: str | None
    max_size: str | None
