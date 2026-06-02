import httpx
from fastapi import APIRouter, HTTPException

from ..core.config import settings
from ..schemas.store import StoreCatalogResponse, StoreItem

router = APIRouter()

@router.get("/", response_model=StoreCatalogResponse)
async def get_stores(size: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.store_catalog_url, params={"size": size})
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    items = [StoreItem(**item) for item in data.get("items", [])]
    return StoreCatalogResponse(size=size, items=items)
