from fastapi import APIRouter, HTTPException

from ..core.config import settings
from ..schemas.payment import SubscriptionRequest, SubscriptionResponse

router = APIRouter()

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe(request: SubscriptionRequest):
    if not settings.stripe_api_key:
        raise HTTPException(status_code=500, detail="Payment gateway not configured")

    return SubscriptionResponse(success=True, message=f"Suscripción activa para {request.email}")
