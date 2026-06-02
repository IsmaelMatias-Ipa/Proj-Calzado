from pydantic import BaseModel, EmailStr


class SubscriptionRequest(BaseModel):
    user_id: str
    email: EmailStr
    plan_id: str


class SubscriptionResponse(BaseModel):
    success: bool
    message: str
