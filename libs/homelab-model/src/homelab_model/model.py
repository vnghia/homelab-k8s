from homelab_types import BaseModel as TypesBaseModel
from homelab_types import RootModel as TypesRootModel


class BaseModel(TypesBaseModel):
    pass


class RootModel[T](TypesRootModel[T]):
    pass
