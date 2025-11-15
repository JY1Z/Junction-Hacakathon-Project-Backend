# app/schemas/models.py
# V1
from typing import List, Optional, Literal
from pydantic import BaseModel


# -------- Customer --------
class CustomerBase(BaseModel):
    name: str
    description: Optional[str] = None
    behavior: Optional[str] = None


# -------- Product --------
class ProductBase(BaseModel):
    name: str
    category: str
    price: Optional[float] = None
    quantity: int


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
    replacement_message: str = ""


class OrderAnalysisResponse(BaseModel):
    order_id: int
    recommendations: List[MissingItemRecommendation]


# -------- Customer decision --------
class ReplacementDecision(BaseModel):
    original_product_id: int
    chosen_product_id: Optional[int]


class OrderDecisionRequest(BaseModel):
    action: Literal["confirm", "reject"]
    decisions: List[ReplacementDecision]


class OrderDecisionResponse(BaseModel):
    order_id: int
    action: str
    decisions: List[ReplacementDecision]
    status: str
    message_to_delivery: str

