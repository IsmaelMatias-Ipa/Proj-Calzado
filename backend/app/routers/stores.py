import httpx
from fastapi import APIRouter, HTTPException

from ..core.config import settings
from ..schemas.store import StoreCatalogResponse, StoreItem

router = APIRouter()

# Base de datos local de calzado para simulación (MVP)
MOCK_PRODUCTS = [
    # Talla 38
    {"id": "s1", "name": "Nike Air Force 1 '07", "price": 119.99, "currency": "USD", "url": "https://www.nike.com", "size": "38", "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500", "vendor": "Nike Store"},
    {"id": "s2", "name": "Adidas Stan Smith Shoes", "price": 95.00, "currency": "USD", "url": "https://www.adidas.com", "size": "38", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "vendor": "Adidas Shop"},
    
    # Talla 39
    {"id": "s3", "name": "Puma Carina Sneaker", "price": 65.00, "currency": "USD", "url": "https://www.puma.com", "size": "39", "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500", "vendor": "Puma Store"},
    {"id": "s4", "name": "Converse Chuck Taylor All Star", "price": 60.00, "currency": "USD", "url": "https://www.converse.com", "size": "39", "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500", "vendor": "Converse Club"},

    # Talla 40
    {"id": "s5", "name": "Nike Air Max 90", "price": 130.00, "currency": "USD", "url": "https://www.nike.com", "size": "40", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "vendor": "Nike Store"},
    {"id": "s6", "name": "New Balance 574", "price": 84.99, "currency": "USD", "url": "https://www.newbalance.com", "size": "40", "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500", "vendor": "Foot Locker"},

    # Talla 41
    {"id": "s7", "name": "Adidas Ultraboost Light", "price": 190.00, "currency": "USD", "url": "https://www.adidas.com", "size": "41", "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500", "vendor": "Adidas Shop"},
    {"id": "s8", "name": "Vans Old Skool Classic", "price": 70.00, "currency": "USD", "url": "https://www.vans.com", "size": "41", "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500", "vendor": "Vans Outlet"},

    # Talla 42
    {"id": "s9", "name": "Nike Jordan Stay Loyal 2", "price": 115.00, "currency": "USD", "url": "https://www.nike.com", "size": "42", "image": "https://images.unsplash.com/photo-1597045566677-8cf032ed6634?w=500", "vendor": "Nike Store"},
    {"id": "s10", "name": "Reebok Club C 85", "price": 85.00, "currency": "USD", "url": "https://www.reebok.com", "size": "42", "image": "https://images.unsplash.com/photo-1600185375483-26d7a4cc7519?w=500", "vendor": "Reebok Hub"},

    # Talla 43
    {"id": "s11", "name": "Adidas NMD_R1 Shoes", "price": 150.00, "currency": "USD", "url": "https://www.adidas.com", "size": "43", "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500", "vendor": "Adidas Shop"},
    {"id": "s12", "name": "Puma Slipstream Retro", "price": 100.00, "currency": "USD", "url": "https://www.puma.com", "size": "43", "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500", "vendor": "Puma Store"},

    # Talla 44
    {"id": "s13", "name": "Nike Pegasus 40 Running", "price": 130.00, "currency": "USD", "url": "https://www.nike.com", "size": "44", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "vendor": "Nike Store"},
    {"id": "s14", "name": "Asics Gel-Kayano 30", "price": 160.00, "currency": "USD", "url": "https://www.asics.com", "size": "44", "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500", "vendor": "Runner World"}
]

@router.get("/", response_model=StoreCatalogResponse)
async def get_stores(size: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(str(settings.store_catalog_url), params={"size": size})
            response.raise_for_status()
            data = response.json()
            items = [StoreItem(**item) for item in data.get("items", [])]
    except httpx.HTTPError:
        # Fallback a catálogo simulado para pruebas locales (MVP)
        matched = [item for item in MOCK_PRODUCTS if item["size"] == size]
        
        # Si no hay calzado en esa talla, generamos dinámicamente dos opciones para que no esté vacío
        if not matched:
            matched = [
                {
                    "id": f"s-dyn-1-{size}",
                    "name": f"Sneaker Classic Pro Talla {size}",
                    "price": 89.99,
                    "currency": "USD",
                    "url": "https://www.example.com",
                    "size": size,
                    "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
                    "vendor": "Multibrand Store"
                },
                {
                    "id": f"s-dyn-2-{size}",
                    "name": f"Running Trainer Air Talla {size}",
                    "price": 124.50,
                    "currency": "USD",
                    "url": "https://www.example.com",
                    "size": size,
                    "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500",
                    "vendor": "Sport Outlet"
                }
            ]
        items = [StoreItem(**item) for item in matched]

    return StoreCatalogResponse(size=size, items=items)

