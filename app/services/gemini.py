# app/services/gemini.py
import json
from google import genai
from app.core.config import settings


fake_order = {
    "order_id": 1,
    "customer_id": 101,
    "items": [
        {"id": 1, "name": "Whole Milk", "quantity": 1, "status": "unavailable", "price": 3.5},
        {"id": 2, "name": "Eggs 12-pack", "quantity": 1, "status": "unavailable", "price": 2.9},
        {"id": 3, "name": "Low-Fat Milk", "quantity": 1, "status": "available", "price": 3.0},
    ]
}

fake_customer = {
    "id": 101,
    "name": "Italian restaurant kitchen",
    "description": "Casual Italian restaurant kitchen. Focus on pasta and pizza dishes.",
    "behavior": '{"frequent_items": ["mozzarella", "tomato sauce"], "preferences": ["same brand cheese", "bulk packs"]}',
}

fake_products = [
    {"id": 1, "name": "Whole Milk",              "category": "Dairy", "price": 3.5, "quantity": 0},
    {"id": 2, "name": "Eggs 12-pack",            "category": "Eggs",  "price": 2.9, "quantity": 0},
    {"id": 3, "name": "Low-Fat Milk",            "category": "Dairy", "price": 3.0, "quantity": 5},
    {"id": 4, "name": "Oat Milk",                "category": "Dairy", "price": 4.2, "quantity": 8},
    {"id": 5, "name": "Soy Milk",                "category": "Dairy", "price": 3.8, "quantity": 3},
    {"id": 6, "name": "Free-range Eggs 12-pack", "category": "Eggs",  "price": 3.5, "quantity": 6},
]


client = genai.Client(api_key=settings.GEMINI_API_KEY)

missing_items = [
    item for item in fake_order["items"]
    if item["status"] == "unavailable"
]

def build_prompt(
    customer: dict,
    missing_product: dict,
    candidates: list[dict],
) -> str:
    return f"""
You are a smart replacement engine for a restaurant kitchen supply system.

The "customer" is a restaurant kitchen.

Kitchen information:
- name: {customer['name']}
- description: {customer['description']}
- behavior: {customer['behavior']}

Missing product (ingredient):
{json.dumps(missing_product, ensure_ascii=False, indent=2)}

Available candidate replacements (same category, in stock):
{json.dumps(candidates, ensure_ascii=False, indent=2)}

Your task:
- Select the best replacement(s) ONLY from the candidate list.
- Explain briefly why these replacements are suitable for a professional kitchen.
- Mention the missing ingredient and what you are replacing it with.

Return ONLY a JSON object in this exact format:

{{
  "replacement_message": "Short human-friendly message about the replacement.",
  "recommended_ids": [3, 4],
  "reason": "Why these replacements fit the kitchen's needs."
}}
"""


def call_gemini(prompt: str) -> dict:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    respond = response.text.strip()
    print("gemini output:", respond)

    start = respond.find("{")
    end = respond.rfind("}")
    if start != -1 and end != -1 and end > start:
        respond_json = respond[start:end+1]
    else:
        respond_json = respond

    try:
        data = json.loads(respond_json)
    except Exception:
        data = {"recommended_ids": [], "reason": "Failed to parse JSON"}

    data.setdefault("recommended_ids", [])
    data.setdefault("reason", "")
    data.setdefault("replacement_message", "")
    return data


all_recommendations: list[dict] = []

for missing_item in missing_items:
    missing_product = next(p for p in fake_products if p["id"] == missing_item["id"])

    candidates = [
        p for p in fake_products
        if p["category"] == missing_product["category"]
        and p["quantity"] > 0
        and p["quantity"] >= missing_item["quantity"]
        and p["id"] != missing_product["id"]
    ]

    if not candidates:
        all_recommendations.append({
            "original_product_id": missing_product["id"],
            "recommended_ids": [],
            "reason": "No available candidates in same category",
        })
        continue

    prompt = build_prompt(fake_customer, missing_product, candidates)
    result = call_gemini(prompt)

    all_recommendations.append({
        "original_product_id": missing_product["id"],
        "recommended_ids": result["recommended_ids"],
        "reason": result["reason"],
        "replacement_message": result["replacement_message"],
    })

print(json.dumps(all_recommendations, indent=2, ensure_ascii=False))
