from pydantic import BaseModel, Field, HttpUrl


class FootMeasurementRequest(BaseModel):
    image_url: HttpUrl
    user_id: str = Field(..., min_length=1)


class FootMeasurementResponse(BaseModel):
    shoe_size: str
    brand_advice: str
    confidence: float
