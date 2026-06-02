from pydantic import AnyUrl, BaseModel
from typing import List


class StoreItem(BaseModel):
    id: str
    name: str
    price: float
    currency: str
    url: AnyUrl
    size: str
    image: AnyUrl
    vendor: str


class StoreCatalogResponse(BaseModel):
    size: str
    items: List[StoreItem]
