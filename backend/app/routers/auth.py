from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..core.security import create_access_token

router = APIRouter()

class SocialLoginRequest(BaseModel):
    provider: str
    token: str

@router.post("/login")
async def social_login(payload: SocialLoginRequest):
    if payload.provider not in {"google", "facebook"}:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    access_token = create_access_token({"sub": payload.provider, "provider": payload.provider})
    return {"access_token": access_token, "token_type": "bearer"}
