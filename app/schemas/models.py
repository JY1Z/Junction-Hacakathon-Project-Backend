# app/schemas/models.py

# app/schemas/models.py
from typing import List, Optional
from pydantic import BaseModel, validator
import json


# -------- Customer --------
class CustomerBase(BaseModel):
    name: str
    description: Optional[str] = None
    behavior: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    class Config:
        orm_mode = True


# -------- Product --------
class ProductBase(BaseModel):
    name: str
    category: str
    price: Optional[float] = None
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


# -------- Order --------
class OrderItem(BaseModel):
    id: int           # product_id
    name: str
    quantity: int
    status: str       # "ordered" / "available" / "unavailable"
    price: float


class OrderBase(BaseModel):
    customer_id: int
    items: List[OrderItem]


class OrderCreate(OrderBase):
    pass


class OrderRead(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    status: str

    class Config:
        orm_mode = True

    @validator("items", pre=True)
    def parse_items(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return []
        return v


# -------- Message --------
class MessageCreate(BaseModel):
    order_id: int
    customer_id: int
    sender_role: str              # "customer" / "delivery" / "system"
    content: str
    confirmation_status: Optional[str] = None  # "agree" / "disagree" / None


class MessageRead(MessageCreate):
    id: int

    class Config:
        orm_mode = True


# -------- Analyze Response --------
class MissingItemRecommendation(BaseModel):
    original_product_id: int
    recommended_ids: List[int]
    reason: str


class OrderAnalysisResponse(BaseModel):
    order_id: int
    recommendations: List[MissingItemRecommendation]
