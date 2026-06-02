from fastapi import APIRouter, HTTPException

from ..core.config import settings
from ..schemas.payment import SubscriptionRequest, SubscriptionResponse

router = APIRouter()

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe(request: SubscriptionRequest):
    if not settings.stripe_api_key:
        # Modo demostración si Stripe no está configurado (MVP)
        return SubscriptionResponse(
            success=True,
            message=f"[DEMO] Suscripción premium activa para {request.email}"
        )

    return SubscriptionResponse(
        success=True, 
        message=f"Suscripción activa para {request.email}"
    )

