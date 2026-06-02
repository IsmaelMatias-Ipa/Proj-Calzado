import httpx
from fastapi import APIRouter, HTTPException

from ..core.config import settings
from ..schemas.measure import FootMeasurementRequest, FootMeasurementResponse

router = APIRouter()

@router.post("/predict", response_model=FootMeasurementResponse)
async def predict_size(request: FootMeasurementRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.ai_service_url}/measure", json=request.model_dump())
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return FootMeasurementResponse(
        shoe_size=payload.get("shoe_size", "N/A"),
        brand_advice=payload.get("brand_advice", ""),
        confidence=payload.get("confidence", 0.0),
    )
