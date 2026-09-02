from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    price: float = Field(gt=0)
    hours: float = Field(gt=0)
    commission_percent: float = Field(ge=0, le=100)
    booster_id: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    price: float
    hours: float
    commission_percent: float
    booster_id: int