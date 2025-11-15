# app/api/routes/orders.py
from fastapi import APIRouter
from app.schemas.models import (
    OrderCreate,
    OrderAnalysisResponse,
    MissingItemRecommendation,
    OrderDecisionRequest,
    OrderDecisionResponse,
)
from app.services.gemini import get_recommendations_for_order

router = APIRouter(tags=["orders"])


@router.post(
    "/delivery/order",
    response_model=OrderAnalysisResponse,
    summary="Create delivery order and get AI recommendations",
)
async def create_delivery_order(order: OrderCreate) -> OrderAnalysisResponse:

    # mock data
    fake_customer = {
        "id": 101,
        "name": "Italian restaurant kitchen",
        "description": "Casual Italian restaurant kitchen. Focus on pasta and pizza dishes.",
        "behavior": '{"frequent_items": ["mozzarella", "tomato sauce"], "preferences": ["same brand cheese", "bulk packs"]}',
    }

    fake_products = [
        {"id": 1, "name": "Whole Milk", "category": "Dairy", "price": 3.5, "quantity": 0},
        {"id": 2, "name": "Eggs 12-pack", "category": "Eggs", "price": 2.9, "quantity": 0},
        {"id": 3, "name": "Low-Fat Milk", "category": "Dairy", "price": 3.0, "quantity": 5},
        {"id": 4, "name": "Oat Milk", "category": "Dairy", "price": 4.2, "quantity": 8},
        {"id": 5, "name": "Soy Milk", "category": "Dairy", "price": 3.8, "quantity": 3},
        {"id": 6, "name": "Free-range Eggs 12-pack", "category": "Eggs", "price": 3.5, "quantity": 6},
    ]

    order_dict = {
        "order_id": 1,
        "customer_id": order.customer_id,
        "items": [item.model_dump() for item in order.items],
    }

    recs_raw = get_recommendations_for_order(
        order=order_dict,
        customer=fake_customer,
        products=fake_products,
    )

    recommendations = [
        MissingItemRecommendation(
            replacement_message=r.get("replacement_message", ""),
            recommended_ids=r.get("recommended_ids", []),
            reason=r.get("reason", ""),
            original_product_id=r.get("original_product_id"),

        )
        for r in recs_raw
    ]

    return OrderAnalysisResponse(
        order_id=order_dict["order_id"],
        recommendations=recommendations,
    )


@router.post(
    "/customer/order/{order_id}/decision",
    response_model=OrderDecisionResponse,
    summary="Customer confirms or rejects replacements",
)
async def customer_decision(
    order_id: int,
    payload: OrderDecisionRequest
) -> OrderDecisionResponse:

    status_map = {
        "confirm": "confirmed",
        "reject": "rejected"
    }

    if payload.action == "confirm":
        message = f"Customer confirmed replacements for order {order_id}."
    else:
        message = (
            f"Customer rejected the replacements for order {order_id}. "
        )

    return OrderDecisionResponse(
        order_id=order_id,
        action=payload.action,
        decisions=payload.decisions,
        status=status_map[payload.action],
        message_to_delivery=message
    )
