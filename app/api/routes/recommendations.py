# app/api/routes/recommendations.py
from fastapi import APIRouter, Depends
from app.services.gemini import (
    get_recommendations_for_order,
    fake_order,
    fake_customer,
    fake_products,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

@router.get("/demo")
async def demo_recommendations():
    result = get_recommendations_for_order(
        order=fake_order,
        customer=fake_customer,
        products=fake_products,
    )
    return {"recommendations": result}
